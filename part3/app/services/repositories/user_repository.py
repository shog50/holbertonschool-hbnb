from models.user import User

class UserRepository:
    """Handles all database operations for Users"""
    
    def __init__(self, session):
        self.session = session
    
    def get(self, user_id):
        return self.session.get(User, user_id)
    
    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()
    
    def get_all(self):
        return self.session.query(User).all()
    
    def create(self, user_data):
        user = User(
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_admin=user_data.get('is_admin', False)
        )
        self.session.add(user)
        self.session.commit()
        return user
    
    def update(self, user_id, updates):
        user = self.get(user_id)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            self.session.commit()
        return user
    
    def delete(self, user_id):
        user = self.get(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
