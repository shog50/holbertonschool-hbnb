import pytest
from app.models.user import User
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_user_valid_and_invalid():
    User._used_emails.clear()
    u1 = User("Alice", "Smith", "alice@example.com")
    assert u1.first_name == "Alice"
    assert not u1.is_admin

    with pytest.raises(ValueError):
        User("X"*51, "Smith", "x@example.com")

    with pytest.raises(ValueError):
        User("Bob", "Y"*51, "y@example.com")

    with pytest.raises(ValueError):
        User("Bob", "Jones", "")

    with pytest.raises(ValueError):
        User("Bob", "Jones", "no-at-symbol")

    u2 = User("Carol", "Lee", "carol@example.com")
    with pytest.raises(ValueError):
        User("Carol", "Lee", "carol@example.com")
