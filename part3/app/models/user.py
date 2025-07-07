from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModel

class User(BaseModel):
    _used_emails = set() 

    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review', back_populates='owner', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        if not email or '@' not in email:
            raise ValueError("Invalid email")
        if email in User._used_emails:
            raise ValueError("Email already used")
        User._used_emails.add(email)

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        if password:
            self.password = password  # uses setter to hash

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
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
        for key, value in data.items():
            if key == 'password':
                self.password = value  # hashed via setter
            elif hasattr(self, key):
                setattr(self, key, value)

    def set_admin(self, is_admin=True):
        self.is_admin = is_admin
        db.session.commit()

    def __repr__(self):
        return f"<User {self.email}>"
