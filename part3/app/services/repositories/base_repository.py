from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseRepository(ABC):
    """Abstract base class defining the repository interface"""
    @abstractmethod
    def get(self, id: str) -> Optional[Any]:
        """Get an entity by id"""
        pass

    @abstractmethod
    def get_by_attribute(self, attribute: str, value: Any) -> Optional[Any]:
        """Get an entity by attribute value"""
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """Get all entities"""
        pass

    @abstractmethod
    def add(self, entity: Any) -> Any:
        """Add a new entity"""
        pass

    @abstractmethod
    def update(self, id: str, updates: Dict[str, Any]) -> Any:
        """Update an existing entity"""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete an entity"""
        pass
