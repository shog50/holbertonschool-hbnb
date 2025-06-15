from flask_restx import Namespace, Resource

api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    def get(self):
        """List all reviews"""
        return {'message': 'Not implemented yet'}, 501

    def post(self):
        """Create a new review"""
        return {'message': 'Not implemented yet'}, 501
