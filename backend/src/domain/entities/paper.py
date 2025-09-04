"""
Paper entity - Core domain model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class PaperSource(Enum):
    ARXIV = "arxiv"
    OPENALEX = "openalex"
    CROSSREF = "crossref"


@dataclass(frozen=True)
class Author:
    """Value object representing a paper author"""
    name: str
    affiliation: Optional[str] = None
    orcid: Optional[str] = None


@dataclass(frozen=True)
class Paper:
    """
    Paper entity - represents a research paper from any source
    Following DDD principles, this is our core domain entity
    """
    id: str
    title: str
    authors: List[Author]
    abstract: str
    source: PaperSource
    published_date: datetime
    url: str
    doi: Optional[str] = None
    categories: List[str] = None
    citation_count: Optional[int] = None
    
    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Paper title cannot be empty")
        if not self.authors:
            raise ValueError("Paper must have at least one author")
        if not self.abstract.strip():
            raise ValueError("Paper abstract cannot be empty")
    
    @property
    def primary_author(self) -> Author:
        """Returns the first author (primary author)"""
        return self.authors[0]
    
    @property
    def formatted_authors(self) -> str:
        """Returns formatted author names for display"""
        if len(self.authors) == 1:
            return self.authors[0].name
        elif len(self.authors) <= 3:
            return ", ".join(author.name for author in self.authors)
        else:
            return f"{self.authors[0].name} et al."
