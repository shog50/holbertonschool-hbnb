from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from uuid import uuid4

class User(db.Model):
    """SQLAlchemy User model with password hashing"""
    tablename = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def init(self, email, password, first_name=None, last_name=None, is_admin=False):
        self.email = email
        self.password = password  # Uses the setter below
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    @property
    def password(self):
        """Prevent password from being accessed directly"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Hash and store the password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        """Update user attributes"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # updated_at is automatically handled by SQLAlchemy

    def set_admin(self, is_admin=True):
        """Set or revoke admin privileges
        
        Args:
            is_admin (bool): True to grant admin, False to revoke
        """
        self.is_admin = is_admin
        db.session.commit()  # Explicit commit since we're bypassing update()
