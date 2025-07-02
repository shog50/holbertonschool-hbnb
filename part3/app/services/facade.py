from sqlalchemy.orm import Session
from models import User, Place, Review, Amenity

class Facade:
    """Complete Facade for all entities with simplified SQLAlchemy integration"""
    
    def init(self, session: Session):
        self.session = session

    # ===== Core CRUD Operations =====
    def add(self, entity):
        """Generic create operation"""
        self.session.add(entity)
        self.session.commit()
        return entity

    def get(self, model, id):
        """Generic get by ID"""
        return self.session.get(model, id)

    def delete(self, entity):
        """Generic delete"""
        self.session.delete(entity)
        self.session.commit()

    def update(self, entity, **updates):
        """Generic update"""
        for key, value in updates.items():
            setattr(entity, key, value)
        self.session.commit()
        return entity

    # ===== User Operations (Task 6 Focus) =====
    def create_user(self, email, password, **kwargs):
        """Create user with password hashing"""
        user = User(email=email, password=password, **kwargs)
        return self.add(user)

    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    # ===== Place Operations =====
    def create_place(self, title, owner_id, **kwargs):
        return self.add(Place(title=title, owner_id=owner_id, **kwargs))

    def get_places_by_owner(self, owner_id):
        return self.session.query(Place).filter_by(owner_id=owner_id).all()

    # ===== Review Operations =====
    def create_review(self, text, user_id, place_id, rating):
        return self.add(Review(
            text=text,
            user_id=user_id,
            place_id=place_id,
            rating=rating
        ))

    def get_reviews_for_place(self, place_id):
        return self.session.query(Review).filter_by(place_id=place_id).all()

    # ===== Amenity Operations =====
    def create_amenity(self, name, description=None):
        return self.add(Amenity(name=name, description=description))

    def get_amenity_by_name(self, name):
        return self.session.query(Amenity).filter_by(name=name).first()
