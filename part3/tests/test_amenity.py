import pytest
from app.models.amenity import Amenity
import io
import contextlib
from app.models.place import Place
from app.models.review import Review
from app.models.user import User

def test_amenity_length():
    ok = Amenity("Parking")
    assert ok.name == "Parking"

    with pytest.raises(ValueError):
        Amenity("X" * 51)

def test_display_methods():
    owner = User("Owner", "One", "owner.display@test.com")
    place = Place("Test", "Desc", 10.0, 0.0, 0.0, owner)

    # Test empty amenities display
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_amenities()
    assert buf.getvalue().strip() == "There are no amenities for this place."

    # Test populated amenities display
    amen = Amenity("Pool")
    place.add_amenity(amen)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_amenities()
    expected_amen = "Amenities:\n - Pool"
    assert buf.getvalue().strip() == expected_amen

    # Test empty reviews display
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_reviews()
    assert buf.getvalue().strip() == "There are no reviews for this place."

    # Test populated reviews display
    rev = Review("Loved it!", 5, place, owner)
    place.add_review(rev)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_reviews()
    expected_rev = "Owner: Loved it!"
    assert buf.getvalue().strip() == expected_rev
