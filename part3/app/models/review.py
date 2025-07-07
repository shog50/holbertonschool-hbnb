from app.extensions import db
from .base_model import BaseModel
from app.models.user import User

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(512), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    place = db.relationship('Place', back_populates='reviews')
    owner = db.relationship('User', back_populates='reviews')

    def __init__(self, text, rating, place, owner):
        from .place import Place

        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        if not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.place = place
        self.owner = owner

    def __repr__(self):
        return f"<Review {self.rating} stars>"
