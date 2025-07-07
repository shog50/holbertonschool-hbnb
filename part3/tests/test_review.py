import pytest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def test_review_validations():
    owner = User("R", "U", "r@example.com")
    p = Place("Place", "", 10.0, 0.0, 0.0, owner)

    with pytest.raises(ValueError):
        Review("Bad", 6, p, owner)

    with pytest.raises(TypeError):
        Review("Text", 3, "not a place", owner)

    with pytest.raises(TypeError):
        Review("Text", 3, p, "not a user")
