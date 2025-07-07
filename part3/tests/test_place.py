import pytest
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def test_place_and_relationships():
    owner = User("Owner", "One", "owner1@example.com")
    p = Place("Cozy Loft", "Nice place", 120.0, 40.0, -75.0, owner)
    assert p.owner is owner

    with pytest.raises(TypeError):
        Place("Title", "Desc", 50, 0, 0, "not a user")

    a = Amenity("Wi-Fi")
    p.add_amenity(a)
    assert p.amenities == [a]

    r = Review("Great stay!", 5, p, owner)
    p.add_review(r)
    assert p.reviews == [r]
