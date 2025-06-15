import uuid
from datetime import datetime

class Review:
    """Review model class"""
    
    def __init__(self, text, user_id, place_id):
        self.id = str(uuid.uuid4())
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
