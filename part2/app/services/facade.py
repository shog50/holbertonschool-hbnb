from app.persistence.repository import InMemoryRepository
import re

class HBnBFacade:
    """Facade for HBnB application services"""
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        if not user_data.get('first_name'):
            raise ValueError("First name is required")
        if not user_data.get('last_name'):
            raise ValueError("Last name is required")
        email = user_data.get('email')
        if not email or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Invalid email format")
        
        user = self.user_repo.create(user_data)
        return user

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise LookupError("Place not found")
        return place

    def create_review(self, review_data):
        if not review_data.get('text'):
            raise ValueError("Review text is required")
        if 'rating' not in review_data or not isinstance(review_data['rating'], int):
            raise ValueError("Rating must be an integer")
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise LookupError("User not found")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise LookupError("Place not found")

        review = self.review_repo.create(review_data)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return review

    def get_all_reviews(self):
        return self.review_repo.list_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.filter_by('place_id', place_id)
        return reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data and not review_data['text']:
            raise ValueError("Review text cannot be empty")
        if 'rating' in review_data:
            if not isinstance(review_data['rating'], int):
                raise ValueError("Rating must be an integer")
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5")
        
        updated_review = self.review_repo.update(review_id, review_data)
        return updated_review

    def delete_review(self, review_id):
        deleted = self.review_repo.delete(review_id)
        return deleted
