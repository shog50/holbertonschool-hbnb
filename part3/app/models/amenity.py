from app.extensions import db
from .base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<Amenity {self.name}>"
