from flask_restx import Namespace, Resource

api = Namespace('places', description='Place operations')

@api.route('/')
class PlaceList(Resource):
    def get(self):
        """List all places"""
        return {'message': 'Not implemented yet'}, 501

    def post(self):
        """Create a new place"""
        return {'message': 'Not implemented yet'}, 501
