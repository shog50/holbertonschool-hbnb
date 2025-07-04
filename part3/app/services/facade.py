from sqlalchemy.orm import Session
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class Facade:
    """Complete Facade for all entities with simplified SQLAlchemy integration"""

    def __init__(self, session: Session):
        self.session = session

    # ===== Core CRUD Operations =====
    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        return entity

    def get(self, model, id):
        return self.session.get(model, id)

    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()

    def update(self, entity, **updates):
        for key, value in updates.items():
            setattr(entity, key, value)
        self.session.commit()
        return entity

    # ===== User Operations =====
    def create_user(self, email, password, **kwargs):
        user = User(email=email, **kwargs)
        user.hash_password(password)
        return self.add(user)

    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    # ===== Place Operations =====
    def create_place(self, title, owner_id, **kwargs):
        place = Place(title=title, owner_id=owner_id, **kwargs)
        return self.add(place)

    def get_places_by_owner(self, owner_id):
        return self.session.query(Place).filter_by(owner_id=owner_id).all()

    # ===== Review Operations =====
    def create_review(self, text, user_id, place_id, rating):
        review = Review(text=text, user_id=user_id, place_id=place_id, rating=rating)
        return self.add(review)

    def get_reviews_for_place(self, place_id):
        return self.session.query(Review).filter_by(place_id=place_id).all()

    # ===== Amenity Operations =====
    def create_amenity(self, name, description=None):
        amenity = Amenity(name=name)
        if description:
            amenity.description = description
        return self.add(amenity)

    def get_amenity_by_name(self, name):
        return self.session.query(Amenity).filter_by(name=name).first()
