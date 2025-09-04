"""
Search Query value object
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class SortBy(Enum):
    RELEVANCE = "relevance"
    DATE = "date"
    CITATIONS = "citations"


@dataclass(frozen=True)
class SearchQuery:
    """
    Value object representing a search query for research papers
    Immutable and contains all search parameters
    """
    query: str
    max_results: int = 5
    sort_by: SortBy = SortBy.RELEVANCE
    sources: Optional[List[str]] = None
    date_from: Optional[str] = None  # YYYY-MM-DD format
    date_to: Optional[str] = None    # YYYY-MM-DD format
    
    def __post_init__(self):
        if not self.query.strip():
            raise ValueError("Search query cannot be empty")
        if self.max_results <= 0 or self.max_results > 50:
            raise ValueError("Max results must be between 1 and 50")
        if self.sources is not None and not self.sources:
            raise ValueError("Sources list cannot be empty if provided")
    
    @property
    def sanitized_query(self) -> str:
        """Returns sanitized query for API calls"""
        return self.query.strip().lower()
    
    @property
    def enabled_sources(self) -> List[str]:
        """Returns list of enabled sources, defaults to all if none specified"""
        return self.sources or ["arxiv", "openalex", "crossref"]
