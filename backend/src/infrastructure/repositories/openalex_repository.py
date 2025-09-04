"""
OpenAlex repository implementation
"""
import httpx
from datetime import datetime
from typing import List, Optional

from ...domain.entities.paper import Paper, Author, PaperSource
from ...domain.repositories.paper_repository import OpenAlexRepository
from ...domain.value_objects.search_query import SearchQuery


class OpenAlexRepositoryImpl(OpenAlexRepository):
    """
    OpenAlex repository implementation using OpenAlex API
    Follows Repository pattern and Single Responsibility Principle
    """
    
    def __init__(self):
        self.base_url = "https://api.openalex.org/works"
        self.timeout = 30.0
    
    async def search_papers(self, search_query: SearchQuery) -> List[Paper]:
        """Search papers from OpenAlex based on query"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = self._build_search_params(search_query)
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                return self._parse_response(data)
        except Exception as e:
            print(f"Error searching OpenAlex: {e}")
            return []
    
    def _build_search_params(self, search_query: SearchQuery) -> dict:
        """Build search parameters for OpenAlex API"""
        params = {
            "search": search_query.query,
            "per-page": search_query.max_results,
            "sort": self._map_sort_by(search_query.sort_by),
            "filter": self._build_filters(search_query)
        }
        return {k: v for k, v in params.items() if v}
    
    def _map_sort_by(self, sort_by) -> str:
        """Map our sort_by enum to OpenAlex sort parameters"""
        mapping = {
            "relevance": "relevance_score:desc",
            "date": "publication_date:desc",
            "citations": "cited_by_count:desc"
        }
        return mapping.get(sort_by.value, "relevance_score:desc")
    
    def _build_filters(self, search_query: SearchQuery) -> Optional[str]:
        """Build filter string for OpenAlex API"""
        filters = []
        
        if search_query.date_from or search_query.date_to:
            date_filter = "publication_date:"
            if search_query.date_from and search_query.date_to:
                date_filter += f"{search_query.date_from}-{search_query.date_to}"
            elif search_query.date_from:
                date_filter += f">{search_query.date_from}"
            elif search_query.date_to:
                date_filter += f"<{search_query.date_to}"
            filters.append(date_filter)
        
        # Only include works with abstracts
        filters.append("has_abstract:true")
        
        return ",".join(filters) if filters else None
    
    def _parse_response(self, data: dict) -> List[Paper]:
        """Parse OpenAlex API response and convert to Paper entities"""
        papers = []
        
        for work in data.get("results", []):
            try:
                paper = self._convert_work_to_paper(work)
                if paper:
                    papers.append(paper)
            except Exception as e:
                print(f"Error parsing OpenAlex work: {e}")
                continue
        
        return papers
    
    def _convert_work_to_paper(self, work: dict) -> Optional[Paper]:
        """Convert OpenAlex work to Paper entity"""
        # Skip works without abstract
        abstract = work.get("abstract")
        if not abstract:
            return None
        
        # Extract authors
        authors = []
        for authorship in work.get("authorships", []):
            author_info = authorship.get("author", {})
            if author_info.get("display_name"):
                authors.append(Author(
                    name=author_info["display_name"],
                    orcid=author_info.get("orcid")
                ))
        
        if not authors:
            return None
        
        # Extract concepts as categories
        categories = []
        for concept in work.get("concepts", [])[:5]:  # Top 5 concepts
            if concept.get("display_name"):
                categories.append(concept["display_name"])
        
        # Parse published date
        pub_date_str = work.get("publication_date")
        if not pub_date_str:
            return None
        
        try:
            published_date = datetime.strptime(pub_date_str, "%Y-%m-%d")
        except ValueError:
            return None
        
        # Get DOI or OpenAlex URL
        doi = work.get("doi")
        url = doi if doi else work.get("id", "")
        
        return Paper(
            id=f"openalex:{work.get('id', '').split('/')[-1]}",
            title=work.get("title", "").strip(),
            authors=authors,
            abstract=abstract.strip(),
            source=PaperSource.OPENALEX,
            published_date=published_date,
            url=url,
            doi=doi,
            categories=categories,
            citation_count=work.get("cited_by_count", 0)
        )
