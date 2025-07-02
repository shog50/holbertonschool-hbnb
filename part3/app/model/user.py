from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from uuid import uuid4

class User:
    def __init__(self, email, password, first_name=None, last_name=None):
        self.id = str(uuid4())
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
