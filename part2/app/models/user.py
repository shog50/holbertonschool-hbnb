from . import BaseModel
from typing import Optional

class User(BaseModel):
    """User model class"""
    
    def __init__(self, email: str, password: str, 
                 first_name: Optional[str] = None, 
                 last_name: Optional[str] = None,
                 **kwargs):
        """
        Initialize User instance
        
        Args:
            email (str): User's email address
            password (str): User's password (will be hashed later)
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name
        """
        super().__init__(**kwargs)
        self.email = email
        self.password = password  # Will be hashed in later implementation
        self.first_name = first_name
        self.last_name = last_name
        self.places = []  # List of places owned by this user
        self.reviews = []  # List of reviews written by this user
        
    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        return '@' in email and '.' in email.split('@')[-1]
    
    def add_place(self, place):
        """Add a place to user's owned places"""
        if place not in self.places:
            self.places.append(place)
    
    def add_review(self, review):
        """Add a review to user's written reviews"""
        if review not in self.reviews:
            self.reviews.append(review)
