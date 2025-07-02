from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class Facade:
    """
    The Facade class provides a unified interface to the underlying repositories.
    It acts as a single entry point for all data access operations.
    """

    def init(self, session: Session):
        """
        Initialize the Facade with a SQLAlchemy session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.user_repo = SQLAlchemyRepository(session, User)
        self.place_repo = SQLAlchemyRepository(session, Place)
        self.review_repo = SQLAlchemyRepository(session, Review)
        self.amenity_repo = SQLAlchemyRepository(session, Amenity)

    # ========== User Operations ==========
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            email: The email address to search for

        Returns:
            User object if found, None otherwise
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> List[User]:
        """
        Retrieve all users in the system.

        Returns:
            List of all User objects
        """
        return self.user_repo.get_all()

    def create_user(self, user_data: Dict) -> User:
        """
        Create a new user.

        Args:
            user_data: Dictionary containing user attributes

        Returns:
            The created User object
        """
        user = User(**user_data)
        return self.user_repo.add(user)

    def update_user(self, user_id: str, updates: Dict) -> Optional[User]:
        """
        Update an existing user.

        Args:
            user_id: ID of the user to update
            updates: Dictionary of attributes to update

        Returns:
            Updated User object if successful, None otherwise
        """
        return self.user_repo.update(user_id, updates)

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.

        Args:
            user_id: ID of the user to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        return self.user_repo.delete(user_id)

    # ========== Place Operations ==========
    def get_place(self, place_id: str) -> Optional[Place]:
        """
        Retrieve a place by ID.

        Args:
            place_id: The ID of the place to retrieve

        Returns:
            Place object if found, None otherwise
        """
        return self.place_repo.get(place_id)

    def get_all_places(self) -> List[Place]:
        """
        Retrieve all places in the system.

        Returns:
            List of all Place objects
        """
        return self.place_repo.get_all()

    def create_place(self, place_data: Dict) -> Place:
        """
        Create a new place.

        Args:
            place_data: Dictionary containing place attributes

        Returns:
            The created Place object
        """
        place = Place(**place_data)
        return self.place_repo.add(place)

    def update_place(self, place_id: str, updates: Dict) -> Optional[Place]:
        """
        Update an existing place.

        Args:
            place_id: ID of the place to update
            updates: Dictionary of attributes to update

        Returns:
            Updated Place object if successful, None otherwise
        """
        return self.place_repo.update(place_id, updates)
    def delete_place(self, place_id: str) -> bool:
        """
        Delete a place.

        Args:
            place_id: ID of the place to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        return self.place_repo.delete(place_id)

    # ========== Review Operations ==========
    def get_review(self, review_id: str) -> Optional[Review]:
        """
        Retrieve a review by ID.

        Args:
            review_id: The ID of the review to retrieve

        Returns:
            Review object if found, None otherwise
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> List[Review]:
        """
        Retrieve all reviews in the system.

        Returns:
            List of all Review objects
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """
        Retrieve all reviews for a specific place.

        Args:
            place_id: ID of the place to get reviews for

        Returns:
            List of Review objects for the specified place
        """
        return self.review_repo.get_by_attribute('place_id', place_id)

    def create_review(self, review_data: Dict) -> Review:
        """
        Create a new review.

        Args:
            review_data: Dictionary containing review attributes

        Returns:
            The created Review object
        """
        review = Review(**review_data)
        return self.review_repo.add(review)

    def update_review(self, review_id: str, updates: Dict) -> Optional[Review]:
        """
        Update an existing review.

        Args:
            review_id: ID of the review to update
            updates: Dictionary of attributes to update

        Returns:
            Updated Review object if successful, None otherwise
        """
        return self.review_repo.update(review_id, updates)

    def delete_review(self, review_id: str) -> bool:
        """
        Delete a review.

        Args:
            review_id: ID of the review to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        return self.review_repo.delete(review_id)

    # ========== Amenity Operations ==========
    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id: The ID of the amenity to retrieve

        Returns:
            Amenity object if found, None otherwise
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> List[Amenity]:
        """
        Retrieve all amenities in the system.

        Returns:
            List of all Amenity objects
        """
        return self.amenity_repo.get_all()

    def create_amenity(self, amenity_data: Dict) -> Amenity:
        """
        Create a new amenity.

        Args:
            amenity_data: Dictionary containing amenity attributes

        Returns:
            The created Amenity object
        """
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def update_amenity(self, amenity_id: str, updates: Dict) -> Optional[Amenity]:
        """
        Update an existing amenity.

        Args:
            amenity_id: ID of the amenity to update
            updates: Dictionary of attributes to update

        Returns:
            Updated Amenity object if successful, None otherwise
        """
        return self.amenity_repo.update(amenity_id, updates)

    def delete_amenity(self, amenity_id: str) -> bool:
        """
        Delete an amenity.

        Args:
            amenity_id: ID of the amenity to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        return self.amenity_repo.delete(amenity_id)
