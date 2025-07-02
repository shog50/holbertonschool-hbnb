from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth import admin_required
from app.services import facade

api = Namespace('users', description='User operations')

# Response model (excludes password hash)
user_response_model = api.model('UserResponse', {
    'id': fields.String(required=True),
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'is_admin': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
})

# Request model (for create/update)
user_request_model = api.model('UserRequest', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'is_admin': fields.Boolean(default=False)
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    @admin_required
    def get(self):
        """List all users (Admin only)"""
        users = facade.user_repo.get_all()
        return [user.to_dict() for user in users]

    @api.expect(user_request_model)
    @api.marshal_with(user_response_model, code=201)
    @admin_required
    def post(self):
        """Create a new user (Admin only)"""
        data = api.payload
        
        # Validate email uniqueness
        if facade.user_repo.get_by_attribute('email', data['email']):
            api.abort(400, "Email already exists")
            
        # Create user
        user = facade.create_user(data)
        return user.to_dict(), 201

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @jwt_required()
    def get(self, user_id):
        """Get user details"""
        current_user_id = get_jwt_identity()['id']
        
        # Users can view their own profile, admins can view any
        if user_id != current_user_id and not facade.user_repo.get(current_user_id).is_admin:
            api.abort(403, "Not authorized to view this user")
            
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
            
        return user.to_dict()

    @api.expect(user_request_model)
    @api.marshal_with(user_response_model)
    @admin_required
    def put(self, user_id):
        """Update any user (Admin only)"""
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
            
        data = api.payload
        
        # Check if email is being changed to an existing one
        if 'email' in data and data['email'] != user.email:
            if facade.user_repo.get_by_attribute('email', data['email']):
                api.abort(400, "Email already exists")
        
        updated_user = facade.update_user(user_id, data)
        return updated_user.to_dict()

    @api.response(204, 'User deleted')
    @admin_required
    def delete(self, user_id):
        """Delete a user (Admin only)"""
        if not facade.user_repo.get(user_id):
            api.abort(404, "User not found")
            
        facade.user_repo.delete(user_id)
        return '', 204

@api.route('/<string:user_id>/admin')
class AdminUser(Resource):
    @api.response(200, 'Admin status updated')
    @admin_required
    def post(self, user_id):
        """Promote/demote user admin status (Admin only)"""
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
            
        is_admin = api.payload.get('is_admin', True)
        user.set_admin(is_admin)
        return {'message': f"User admin status set to {is_admin}"}, 200
