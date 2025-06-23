import uuid
from datetime import datetime

class BaseModel:
    """Base model with id, timestamps, serialization, and updates."""

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())

        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)

    def save(self):
        """Refresh the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes from dictionary and refresh updated_at."""
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue  # don't allow updating these
            setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return dictionary representation for serialization."""
        result = self.__dict__.copy()
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result
