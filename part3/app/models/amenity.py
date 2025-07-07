from app.extensions import db
from .base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name too long")
        self.name = name

    def __repr__(self):
        return f"<Amenity {self.name}>"
