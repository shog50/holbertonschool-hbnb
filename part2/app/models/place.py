from . import BaseModel
from typing import Optional, List

class Place(BaseModel):
    """Place model class"""
    
    def __init__(self, name: str, description: str, owner_id: str,
                 city: Optional[str] = None,
                 address: Optional[str] = None,
                 latitude: Optional[float] = None,
                 longitude: Optional[float] = None,
                 price_per_night: Optional[float] = None,
                 max_guests: Optional[int] = None,
                 **kwargs):
        """
        Initialize Place instance
        
        Args:
            name (str): Name of the place
            description (str): Description of the place
            owner_id (str): ID of the user who owns this place
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.city = city
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = []  # List of amenity IDs
        self.reviews = []  # List of review IDs
        
        # Validate coordinates if provided
        if latitude is not None and longitude is not None:
            self.validate_coordinates(latitude, longitude)
    
    def validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """Validate latitude and longitude values"""
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return True
    
    def add_amenity(self, amenity_id: str):
        """Add an amenity to this place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
    
    def remove_amenity(self, amenity_id: str):
        """Remove an amenity from this place"""
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
    
    def add_review(self, review_id: str):
        """Add a review to this place"""
        if review_id not in self.reviews:
            self.reviews.append(review_id)
