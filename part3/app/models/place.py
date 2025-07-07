from app.extensions import db
from .base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='places')

    amenities = db.relationship('Amenity', secondary=place_amenities, backref='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')

    def __init__(self, title, description, price, latitude, longitude, owner):
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def display_amenities(self):
        if not self.amenities:
            print("There are no amenities for this place.")
        else:
            print("Amenities:")
            for amenity in self.amenities:
                print(f" - {amenity.name}")

    def display_reviews(self):
        if not self.reviews:
            print("There are no reviews for this place.")
        else:
            for review in self.reviews:
                print(f"{review.owner.first_name}: {review.text}")

    def __repr__(self):
        return f"<Place {self.title}>"
