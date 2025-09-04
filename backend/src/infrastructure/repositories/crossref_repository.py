"""
Crossref repository implementation
"""
import httpx
from datetime import datetime
from typing import List, Optional

from ...domain.entities.paper import Paper, Author, PaperSource
from ...domain.repositories.paper_repository import CrossrefRepository
from ...domain.value_objects.search_query import SearchQuery


class CrossrefRepositoryImpl(CrossrefRepository):
    """
    Crossref repository implementation using Crossref API
    Follows Repository pattern and Single Responsibility Principle
    """
    
    def __init__(self):
        self.base_url = "https://api.crossref.org/works"
        self.timeout = 30.0
    
    async def search_papers(self, search_query: SearchQuery) -> List[Paper]:
        """Search papers from Crossref based on query"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = self._build_search_params(search_query)
                headers = {"User-Agent": "Hedwig/1.0 (mailto:research@hedwig.com)"}
                
                response = await client.get(
                    self.base_url, 
                    params=params, 
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                return self._parse_response(data)
        except Exception as e:
            print(f"Error searching Crossref: {e}")
            return []
    
    def _build_search_params(self, search_query: SearchQuery) -> dict:
        """Build search parameters for Crossref API"""
        params = {
            "query": search_query.query,
            "rows": search_query.max_results,
            "sort": self._map_sort_by(search_query.sort_by),
            "filter": self._build_filters(search_query)
        }
        return {k: v for k, v in params.items() if v}
    
    def _map_sort_by(self, sort_by) -> str:
        """Map our sort_by enum to Crossref sort parameters"""
        mapping = {
            "relevance": "relevance",
            "date": "published",
            "citations": "is-referenced-by-count"
        }
        return mapping.get(sort_by.value, "relevance")
    
    def _build_filters(self, search_query: SearchQuery) -> Optional[str]:
        """Build filter string for Crossref API"""
        filters = []
        
        # Only include journal articles and conference papers
        filters.append("type:journal-article,type:proceedings-article")
        
        # Filter by date range if provided
        if search_query.date_from:
            filters.append(f"from-pub-date:{search_query.date_from}")
        if search_query.date_to:
            filters.append(f"until-pub-date:{search_query.date_to}")
        
        # Only include works with abstracts
        filters.append("has-abstract:true")
        
        return ",".join(filters) if filters else None
    
    def _parse_response(self, data: dict) -> List[Paper]:
        """Parse Crossref API response and convert to Paper entities"""
        papers = []
        
        message = data.get("message", {})
        items = message.get("items", [])
        
        for item in items:
            try:
                paper = self._convert_item_to_paper(item)
                if paper:
                    papers.append(paper)
            except Exception as e:
                print(f"Error parsing Crossref item: {e}")
                continue
        
        return papers
    
    def _convert_item_to_paper(self, item: dict) -> Optional[Paper]:
        """Convert Crossref item to Paper entity"""
        # Skip items without abstract
        abstract = item.get("abstract")
        if not abstract:
            return None
        
        # Extract title
        title_list = item.get("title", [])
        if not title_list:
            return None
        title = title_list[0].strip()
        
        # Extract authors
        authors = []
        for author_info in item.get("author", []):
            given = author_info.get("given", "")
            family = author_info.get("family", "")
            if family:
                name = f"{given} {family}".strip()
                affiliation = None
                if author_info.get("affiliation"):
                    affiliation = author_info["affiliation"][0].get("name")
                
                authors.append(Author(
                    name=name,
                    affiliation=affiliation,
                    orcid=author_info.get("ORCID")
                ))
        
        if not authors:
            return None
        
        # Extract categories from subject areas
        categories = item.get("subject", [])[:5]  # Limit to 5 categories
        
        # Parse published date
        published_parts = item.get("published-print") or item.get("published-online")
        if not published_parts or not published_parts.get("date-parts"):
            return None
        
        try:
            date_parts = published_parts["date-parts"][0]
            if len(date_parts) >= 3:
                published_date = datetime(date_parts[0], date_parts[1], date_parts[2])
            elif len(date_parts) >= 2:
                published_date = datetime(date_parts[0], date_parts[1], 1)
            else:
                published_date = datetime(date_parts[0], 1, 1)
        except (ValueError, IndexError):
            return None
        
        # Get DOI and URL
        doi = item.get("DOI")
        url = f"https://doi.org/{doi}" if doi else item.get("URL", "")
        
        return Paper(
            id=f"crossref:{doi}" if doi else f"crossref:{item.get('URL', '')}",
            title=title,
            authors=authors,
            abstract=abstract.strip(),
            source=PaperSource.CROSSREF,
            published_date=published_date,
            url=url,
            doi=doi,
            categories=categories,
            citation_count=item.get("is-referenced-by-count", 0)
        )
