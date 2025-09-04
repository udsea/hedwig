"""
ArXiv repository implementation
"""
import httpx
import feedparser
from datetime import datetime
from typing import List
from urllib.parse import quote

from ...domain.entities.paper import Paper, Author, PaperSource
from ...domain.repositories.paper_repository import ArxivRepository
from ...domain.value_objects.search_query import SearchQuery


class ArxivRepositoryImpl(ArxivRepository):
    """
    ArXiv repository implementation using arXiv API
    Follows Repository pattern and Single Responsibility Principle
    """
    
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.timeout = 30.0
    
    async def search_papers(self, search_query: SearchQuery) -> List[Paper]:
        """Search papers from arXiv based on query"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = self._build_search_params(search_query)
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                return self._parse_response(response.text)
        except Exception as e:
            # In production, you'd want proper logging here
            print(f"Error searching arXiv: {e}")
            return []
    
    def _build_search_params(self, search_query: SearchQuery) -> dict:
        """Build search parameters for arXiv API"""
        # ArXiv search query format: search_query=all:traffic+AND+all:networks
        formatted_query = self._format_query_for_arxiv(search_query.query)
        
        params = {
            "search_query": formatted_query,
            "start": 0,
            "max_results": search_query.max_results,
            "sortBy": self._map_sort_by(search_query.sort_by),
            "sortOrder": "descending"
        }
        return params
    
    def _format_query_for_arxiv(self, query: str) -> str:
        """Format search query for arXiv API"""
        # Split query into words and search in title, abstract, and comments
        words = query.strip().split()
        if len(words) == 1:
            return f"all:{words[0]}"
        
        # For multi-word queries, search for all words
        formatted_words = [f"all:{word}" for word in words]
        return "+AND+".join(formatted_words)
    
    def _map_sort_by(self, sort_by) -> str:
        """Map our sort_by enum to arXiv sort parameters"""
        mapping = {
            "relevance": "relevance",
            "date": "submittedDate",
            "citations": "relevance"  # arXiv doesn't have citation sorting
        }
        return mapping.get(sort_by.value, "relevance")
    
    def _parse_response(self, response_text: str) -> List[Paper]:
        """Parse arXiv API response and convert to Paper entities"""
        feed = feedparser.parse(response_text)
        papers = []
        
        for entry in feed.entries:
            try:
                paper = self._convert_entry_to_paper(entry)
                papers.append(paper)
            except Exception as e:
                print(f"Error parsing arXiv entry: {e}")
                continue
        
        return papers
    
    def _convert_entry_to_paper(self, entry) -> Paper:
        """Convert arXiv entry to Paper entity"""
        # Extract authors
        authors = []
        for author in entry.authors:
            authors.append(Author(name=author.name))
        
        # Extract categories
        categories = []
        if hasattr(entry, 'tags'):
            categories = [tag.term for tag in entry.tags]
        
        # Parse published date
        published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
        
        # Extract arXiv ID from the entry ID
        arxiv_id = entry.id.split("/")[-1]
        
        return Paper(
            id=f"arxiv:{arxiv_id}",
            title=entry.title.replace("\n", " ").strip(),
            authors=authors,
            abstract=entry.summary.replace("\n", " ").strip(),
            source=PaperSource.ARXIV,
            published_date=published_date,
            url=entry.link,
            categories=categories
        )
