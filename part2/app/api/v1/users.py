from flask_restx import Namespace, Resource

api = Namespace('users', description='User operations')

@api.route('/')
class UserList(Resource):
    def get(self):
        """List all users"""
        return {'message': 'Not implemented yet'}, 501

    def post(self):
        """Create a new user"""
        return {'message': 'Not implemented yet'}, 501
