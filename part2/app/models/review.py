from app.models.base_model import BaseModel
from typing import Optional

class Review(BaseModel):
    """Review model class"""
    
    def __init__(self, text: str, user_id: str, place_id: str,
                 rating: Optional[int] = None,
                 **kwargs):
        """
        Initialize Review instance
        
        Args:
            text (str): Review text content
            user_id (str): ID of the user who wrote the review
            place_id (str): ID of the place being reviewed
            rating (int, optional): Rating from 1 to 5
        """
        super().__init__(**kwargs)
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        
        if rating is not None:
            self.validate_rating(rating)
    
    def validate_rating(self, rating: int) -> bool:
        """Validate rating is between 1 and 5"""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return True
    
    def update_text(self, new_text: str):
        """Update review text"""
        self.text = new_text
        self.save()
    
    def update_rating(self, new_rating: int):
        """Update review rating"""
        self.validate_rating(new_rating)
        self.rating = new_rating
        self.save()
