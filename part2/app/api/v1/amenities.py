from flask_restx import Namespace, Resource, fields, abort
from app.services import facade as hbnb_facade
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

# Input/Output Models
amenity_input_model = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Amenity name'),
    'description': fields.String(description='Optional description')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'description': fields.String(description='Description'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """List all amenities"""
        try:
            amenities = hbnb_facade.get_all_amenities()
            return amenities, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('create_amenity')
    @api.expect(amenity_input_model)
    @api.response(400, 'Invalid input')
    @api.response(201, 'Amenity created')
    @api.marshal_with(amenity_response_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = api.payload
        if not data.get('name'):
            abort(400, 'Name is required')

        try:
            amenity = hbnb_facade.create_amenity(data)
            return amenity, 201
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity by ID"""
        try:
            amenity = hbnb_facade.get_amenity(amenity_id)
            if not amenity:
                abort(404, 'Amenity not found')
            return amenity, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('update_amenity')
    @api.expect(amenity_input_model)
    @api.response(400, 'Invalid input')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update amenity details"""
        data = api.payload
        try:
            amenity = hbnb_facade.update_amenity(amenity_id, data)
            if not amenity:
                abort(404, 'Amenity not found')
            return amenity, 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))
