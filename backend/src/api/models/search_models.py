"""
API models for search endpoints
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class SortByAPI(str, Enum):
    RELEVANCE = "relevance"
    DATE = "date"
    CITATIONS = "citations"


class SearchRequest(BaseModel):
    """Request model for paper search"""
    query: str = Field(..., min_length=1, max_length=500, description="Research problem or topic to search for")
    max_results: int = Field(default=5, ge=1, le=50, description="Maximum number of results to return")
    sort_by: SortByAPI = Field(default=SortByAPI.RELEVANCE, description="Sort criteria for results")
    sources: Optional[List[str]] = Field(default=None, description="Sources to search (arxiv, openalex, crossref)")
    date_from: Optional[str] = Field(default=None, description="Start date filter (YYYY-MM-DD)")
    date_to: Optional[str] = Field(default=None, description="End date filter (YYYY-MM-DD)")
    
    @validator('sources')
    def validate_sources(cls, v):
        if v is not None:
            valid_sources = {"arxiv", "openalex", "crossref"}
            invalid_sources = set(v) - valid_sources
            if invalid_sources:
                raise ValueError(f"Invalid sources: {invalid_sources}. Valid sources are: {valid_sources}")
        return v
    
    @validator('date_from', 'date_to')
    def validate_date_format(cls, v):
        if v is not None:
            try:
                from datetime import datetime
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class AuthorResponse(BaseModel):
    """Response model for paper author"""
    name: str
    affiliation: Optional[str] = None
    orcid: Optional[str] = None


class PaperResponse(BaseModel):
    """Response model for paper"""
    id: str
    title: str
    authors: List[AuthorResponse]
    abstract: str
    source: str
    source_name: str
    published_date: str
    url: str
    doi: Optional[str] = None
    categories: Optional[List[str]] = None
    citation_count: Optional[int] = None
    formatted_authors: str
    primary_author: AuthorResponse


class SourceResult(BaseModel):
    """Response model for source-specific results"""
    papers: List[PaperResponse]
    count: int
    error: Optional[str] = None


class SearchResponse(BaseModel):
    """Response model for search results"""
    query: str
    total_results: int
    papers: List[PaperResponse]
    sources: dict  # Dict[str, SourceResult] but keeping flexible for JSON
    search_params: dict


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str
