"""
Paper search service - Application layer
Orchestrates paper search across multiple repositories
"""
import asyncio
from typing import List, Dict, Any
from dataclasses import asdict

from ...domain.entities.paper import Paper
from ...domain.repositories.paper_repository import PaperRepository
from ...domain.value_objects.search_query import SearchQuery
from ...infrastructure.repositories.arxiv_repository import ArxivRepositoryImpl
from ...infrastructure.repositories.openalex_repository import OpenAlexRepositoryImpl
from ...infrastructure.repositories.crossref_repository import CrossrefRepositoryImpl


class PaperSearchService:
    """
    Application service for searching papers across multiple sources
    Follows Single Responsibility Principle and orchestrates domain operations
    """
    
    def __init__(self):
        self.repositories: Dict[str, PaperRepository] = {
            "arxiv": ArxivRepositoryImpl(),
            "openalex": OpenAlexRepositoryImpl(),
            "crossref": CrossrefRepositoryImpl()
        }
    
    async def search_papers(self, search_query: SearchQuery) -> Dict[str, Any]:
        """
        Search papers from enabled sources and return aggregated results
        """
        # Create search tasks for enabled sources
        search_tasks = []
        enabled_sources = search_query.enabled_sources
        
        for source in enabled_sources:
            if source in self.repositories:
                repository = self.repositories[source]
                task = asyncio.create_task(
                    self._safe_search(repository, search_query, source)
                )
                search_tasks.append(task)
        
        # Execute all searches concurrently
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Aggregate results
        all_papers = []
        source_results = {}
        
        for i, result in enumerate(results):
            source = enabled_sources[i] if i < len(enabled_sources) else "unknown"
            
            if isinstance(result, Exception):
                print(f"Error in {source} search: {result}")
                source_results[source] = {"papers": [], "error": str(result)}
            else:
                papers = result
                all_papers.extend(papers)
                source_results[source] = {
                    "papers": [self._paper_to_dict(paper) for paper in papers],
                    "count": len(papers)
                }
        
        # Sort and deduplicate papers
        unique_papers = self._deduplicate_papers(all_papers)
        sorted_papers = self._sort_papers(unique_papers, search_query.sort_by)
        
        # Limit results
        limited_papers = sorted_papers[:search_query.max_results]
        
        return {
            "query": search_query.query,
            "total_results": len(limited_papers),
            "papers": [self._paper_to_dict(paper) for paper in limited_papers],
            "sources": source_results,
            "search_params": {
                "max_results": search_query.max_results,
                "sort_by": search_query.sort_by.value,
                "sources": enabled_sources
            }
        }
    
    async def _safe_search(
        self, 
        repository: PaperRepository, 
        search_query: SearchQuery, 
        source: str
    ) -> List[Paper]:
        """
        Safely execute search with error handling
        """
        try:
            return await repository.search_papers(search_query)
        except Exception as e:
            print(f"Error searching {source}: {e}")
            return []
    
    def _paper_to_dict(self, paper: Paper) -> Dict[str, Any]:
        """Convert Paper entity to dictionary for API response"""
        paper_dict = asdict(paper)
        
        # Convert datetime to ISO string
        if paper_dict.get("published_date"):
            paper_dict["published_date"] = paper.published_date.isoformat()
        
        # Add formatted fields
        paper_dict["formatted_authors"] = paper.formatted_authors
        paper_dict["primary_author"] = asdict(paper.primary_author)
        paper_dict["source_name"] = paper.source.value
        
        return paper_dict
    
    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """
        Remove duplicate papers based on title similarity and DOI
        """
        seen_titles = set()
        seen_dois = set()
        unique_papers = []
        
        for paper in papers:
            # Check DOI first (most reliable)
            if paper.doi and paper.doi in seen_dois:
                continue
            
            # Check title similarity (simple approach)
            normalized_title = paper.title.lower().strip()
            if normalized_title in seen_titles:
                continue
            
            # Add to unique set
            unique_papers.append(paper)
            seen_titles.add(normalized_title)
            if paper.doi:
                seen_dois.add(paper.doi)
        
        return unique_papers
    
    def _sort_papers(self, papers: List[Paper], sort_by) -> List[Paper]:
        """Sort papers based on the specified criteria"""
        if sort_by.value == "date":
            return sorted(papers, key=lambda p: p.published_date, reverse=True)
        elif sort_by.value == "citations":
            return sorted(
                papers, 
                key=lambda p: p.citation_count or 0, 
                reverse=True
            )
        else:  # relevance - keep original order from APIs
            return papers
