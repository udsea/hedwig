"""
Search API routes
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from ..models.search_models import SearchRequest, SearchResponse, SortByAPI
from ...application.services.paper_search_service import PaperSearchService
from ...domain.value_objects.search_query import SearchQuery, SortBy

router = APIRouter(prefix="/api/search", tags=["search"])

# Initialize service
paper_search_service = PaperSearchService()


@router.post("/papers", response_model=SearchResponse)
async def search_papers(request: SearchRequest) -> SearchResponse:
    """
    Search for research papers across multiple sources
    
    This endpoint allows you to search for papers related to specific research problems
    or topics. For example, searching for "traffic networks" will return papers about
    spatial-temporal analysis of traffic networks, traffic flow optimization, etc.
    """
    try:
        # Convert API model to domain value object
        domain_sort_by = SortBy(request.sort_by.value)
        search_query = SearchQuery(
            query=request.query,
            max_results=request.max_results,
            sort_by=domain_sort_by,
            sources=request.sources,
            date_from=request.date_from,
            date_to=request.date_to
        )
        
        # Execute search
        results = await paper_search_service.search_papers(search_query)
        
        return SearchResponse(**results)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/papers", response_model=SearchResponse)
async def search_papers_get(
    query: str = Query(..., description="Research problem or topic to search for"),
    max_results: int = Query(default=5, ge=1, le=50, description="Maximum number of results"),
    sort_by: SortByAPI = Query(default=SortByAPI.RELEVANCE, description="Sort criteria"),
    sources: Optional[str] = Query(default=None, description="Comma-separated sources (arxiv,openalex,crossref)"),
    date_from: Optional[str] = Query(default=None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(default=None, description="End date (YYYY-MM-DD)")
) -> SearchResponse:
    """
    Search for research papers using GET request
    
    Alternative endpoint for searching papers using query parameters.
    Useful for direct browser access or simple integrations.
    """
    # Parse sources if provided
    sources_list = None
    if sources:
        sources_list = [s.strip() for s in sources.split(",")]
    
    # Create request object and delegate to POST endpoint
    request = SearchRequest(
        query=query,
        max_results=max_results,
        sort_by=sort_by,
        sources=sources_list,
        date_from=date_from,
        date_to=date_to
    )
    
    return await search_papers(request)
