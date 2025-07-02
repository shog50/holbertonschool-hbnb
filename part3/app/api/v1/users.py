from flask_restx import Namespace, Resource, fields, abort
from werkzeug.security import generate_password_hash
from app.services.facade import facade as hbnb_facade
from app.models.user import User

api = Namespace('users', description='User operations')

# Request Models
user_input_model = api.model('UserInput', {
    'email': fields.String(required=True, 
                         pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                         description='Valid email address'),
    'password': fields.String(required=True,
                            min_length=8,
                            max_length=128,
                            description='Password (8-128 characters)'),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
})

user_update_model = api.model('UserUpdate', {
    'email': fields.String(pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
    'first_name': fields.String(),
    'last_name': fields.String()
})

# Response Model (never includes password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users (without sensitive data)"""
        users = hbnb_facade.user_repo.get_all()
        return [user.to_dict() for user in users]

    @api.doc('create_user',
             responses={
                 201: 'Success',
                 400: 'Validation Error',
                 409: 'Email exists'
             })
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Create a new user with hashed password"""
        data = api.payload
        
        # Validate required fields
        if not all(k in data for k in ['email', 'password', 'first_name', 'last_name']):
            abort(400, 'All fields are required')
        
        # Check for existing user
        if hbnb_facade.user_repo.get_by_attribute('email', data['email']):
            abort(409, 'Email already registered')
        
        try:
            # User model automatically hashes the password
            user = User(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            hbnb_facade.user_repo.add(user)
            return user.to_dict(), 201
        except ValueError as e:
            abort(400, str(e))

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
        return user.to_dict()

    @api.doc('update_user',
             responses={
                 200: 'Success',
                 400: 'Validation Error',
                 404: 'Not Found',
                 409: 'Email exists'
             })
    @api.expect(user_update_model)
    @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update user information"""
        user = hbnb_facade.user_repo.get(user_id)
        if not user:
            abort(404, 'User not found')
        
        data = api.payload
        
        # Validate email if being changed
        if 'email' in data and data['email'] != user.email:
            if hbnb_facade.user_repo.get_by_attribute('email', data['email']):
                abort(409, 'Email already registered')
        
        # Update allowed fields
        updates = {k: v for k, v in data.items() 
                 if k in ['email', 'first_name', 'last_name']}
        
        hbnb_facade.user_repo.update(user_id, updates)
        updated_user = hbnb_facade.user_repo.get(user_id)
        
        return updated_user.to_dict()
