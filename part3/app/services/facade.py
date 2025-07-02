class HBnBFacade:
    # ... existing code ...
    
    def create_user(self, user_data, is_admin=False):
        """Admin-only user creation"""
        if is_admin and not user_data.get('is_admin'):
            user_data['is_admin'] = True
            
        user = User(**user_data)
        self.user_repo.add(user)
        return user
        
    def update_user(self, user_id, user_data):
        """Admin-only user updates"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
            
        for key, value in user_data.items():
            setattr(user, key, value)
            
        user.save()
        return user
