from typing import List, Dict, Any, Optional, Type
from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository

class SQLAlchemyRepository(BaseRepository):
    """SQLAlchemy implementation of the repository interface"""
    
    def init(self, session: Session, model_class: Type):
        """
        Initialize the repository with a SQLAlchemy session and model class
        
        Args:
            session: SQLAlchemy session
            model_class: SQLAlchemy model class
        """
        self.session = session
        self.model_class = model_class

    def get(self, id: str) -> Optional[Any]:
        """Get an entity by id using SQLAlchemy's get() method"""
        return self.session.get(self.model_class, id)

    def get_by_attribute(self, attribute: str, value: Any) -> Optional[Any]:
        """Get an entity by attribute value using SQLAlchemy's query interface"""
        return self.session.query(self.model_class).filter(
            getattr(self.model_class, attribute) == value
        ).first()

    def get_all(self) -> List[Any]:
        """Get all entities using SQLAlchemy's query interface"""
        return self.session.query(self.model_class).all()

    def add(self, entity: Any) -> Any:
        """Add a new entity using SQLAlchemy's session"""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, id: str, updates: Dict[str, Any]) -> Any:
        """Update an existing entity using SQLAlchemy's session"""
        entity = self.get(id)
        if entity:
            for key, value in updates.items():
                setattr(entity, key, value)
            self.session.commit()
            self.session.refresh(entity)
        return entity

    def delete(self, id: str) -> bool:
        """Delete an entity using SQLAlchemy's session"""
        entity = self.get(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False
