from typing import Optional
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model class"""
    
    def __init__(self, name: str, description: Optional[str] = None, **kwargs):
        """
        Initialize Amenity instance
        
        Args:
            name (str): Name of the amenity
            description (str, optional): Description of the amenity
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.places = []  # List of place IDs that have this amenity
    
    def add_to_place(self, place_id: str):
        """Add this amenity to a place"""
        if place_id not in self.places:
            self.places.append(place_id)
    
    def remove_from_place(self, place_id: str):
        """Remove this amenity from a place"""
        if place_id in self.places:
            self.places.remove(place_id)
