from flask import Blueprint
from flask_restx import Api, Resource, fields
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.services.facade import facade as hbnb_facade

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp, title='Auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """User login to get JWT token"""
        data = api.payload
        user = hbnb_facade.user_repo.get_by_attribute('email', data['email'])
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return {'message': 'Invalid credentials'}, 401
            
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
