import uuid
from datetime import datetime

class Place:
    """Place model class"""
    
    def __init__(self, name, description, owner_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
