from flask_restx import Namespace, Resource

api = Namespace('amenities', description='Amenity operations')

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """List all amenities"""
        return {'message': 'Not implemented yet'}, 501

    def post(self):
        """Create a new amenity"""
        return {'message': 'Not implemented yet'}, 501
