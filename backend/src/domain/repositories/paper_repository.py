"""
Paper repository interface - Following DDD and Dependency Inversion Principle
"""
from abc import ABC, abstractmethod
from typing import List
from ..entities.paper import Paper
from ..value_objects.search_query import SearchQuery


class PaperRepository(ABC):
    """
    Abstract repository interface for paper search operations
    This follows the Repository pattern and Dependency Inversion Principle
    """
    
    @abstractmethod
    async def search_papers(self, search_query: SearchQuery) -> List[Paper]:
        """
        Search for papers based on the provided query
        Returns a list of Paper entities
        """
        pass


class ArxivRepository(PaperRepository):
    """Interface for arXiv paper repository"""
    pass


class OpenAlexRepository(PaperRepository):
    """Interface for OpenAlex paper repository"""
    pass


class CrossrefRepository(PaperRepository):
    """Interface for Crossref paper repository"""
    pass
