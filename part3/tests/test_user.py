import pytest
from app.models.user import User

def test_user_valid_and_invalid():
    # Clear the set before each test to avoid email conflicts
    User._used_emails.clear()

    # Create a valid user
    u1 = User("Alice", "Smith", "alice@example.com", "password123")
    assert u1.first_name == "Alice"
    assert not u1.is_admin
    assert u1.email == "alice@example.com"
    assert u1.verify_password("password123")
    
    # Empty email should raise ValueError
    with pytest.raises(ValueError):
        User("Bob", "Jones", "", "password")

    # Email without '@' should raise ValueError
    with pytest.raises(ValueError):
        User("Bob", "Jones", "no-at-symbol", "password")

    # Duplicate email should raise ValueError
    u2 = User("Carol", "Lee", "carol@example.com", "password456")
    with pytest.raises(ValueError):
        User("Carol", "Lee", "carol@example.com", "password789")

