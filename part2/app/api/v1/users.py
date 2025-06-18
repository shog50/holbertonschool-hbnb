from flask_restx import Namespace, Resource, fields, abort
from app.services.facade import facade as hbnb_facade
from app.models.user import User

api = Namespace('users', description='User operations')

# Input model for user creation (with password)
user_input_model = api.model('UserInput', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# Input model for user updates (without password)
user_update_model = api.model('UserUpdate', {
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# Response model (never includes password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

def sanitize_user(user):
    """Remove sensitive information from user object"""
    if hasattr(user, 'password'):
        delattr(user, 'password')
    return user

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """Get list of all users"""
        users = hbnb_facade.user_repo.get_all()
        return [sanitize_user(user) for user in users]

    @api.doc('create_user')
    @api.expect(user_input_model)
    @api.response(400, 'Invalid input or email exists')
    @api.response(201, 'User created successfully')
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        
        # Validate fields
        if not all(k in data for k in ['email', 'password']):
            abort(400, 'Email and password are required')
        
        # exist user
        if hbnb_facade.user_repo.get_by_attribute('email', data['email']):
            abort(400, 'Email already registered')
        
        # Create and save user
        user = User(
            email=data['email'],
            password=data['password'],  # hash 
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        hbnb_facade.user_repo.add(user)
        
        return sanitize_user(user), 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = hbnb_facade.user_repo.get(user_id)
        if not user:
            abort(404, 'User not found')
        return sanitize_user(user)

    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.response(400, 'Invalid input or email exists')
    @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update user information"""
        user = hbnb_facade.user_repo.get(user_id)
        if not user:
            abort(404, 'User not found')
        
        data = api.payload
        
        # Validate email 
        if 'email' in data and data['email'] != user.email:
            if hbnb_facade.user_repo.get_by_attribute('email', data['email']):
                abort(400, 'Email already registered')
        
        # Update fields
        updates = {k: v for k, v in data.items() 
                 if k in ['email', 'first_name', 'last_name']}
        
        hbnb_facade.user_repo.update(user_id, updates)
        updated_user = hbnb_facade.user_repo.get(user_id)
        
        return sanitize_user(updated_user)

