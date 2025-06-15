import uuid
from datetime import datetime

class User:
    """User model class"""
    
    def __init__(self, email, password, first_name=None, last_name=None):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
