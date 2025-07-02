from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade as hbnb_facade
from app.services.auth import admin_required

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
        """List all amenities (public)"""
        try:
            amenities = hbnb_facade.get_all_amenities()
            return amenities, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('create_amenity', security='apikey')
    @api.expect(amenity_input_model)
    @api.response(400, 'Invalid input')
    @api.response(403, 'Forbidden')
    @api.response(201, 'Amenity created')
    @api.marshal_with(amenity_response_model, code=201)
    @admin_required
    def post(self):
        """Create a new amenity (admin only)"""
        data = api.payload
        if not data.get('name'):
            abort(400, 'Name is required')

        try:
            # Check if amenity already exists
            if hbnb_facade.get_amenity_by_name(data['name']):
                abort(400, 'Amenity with this name already exists')
                
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
        """Get amenity by ID (public)"""
        try:
            amenity = hbnb_facade.get_amenity(amenity_id)
            if not amenity:
                abort(404, 'Amenity not found')
            return amenity, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('update_amenity', security='apikey')
    @api.expect(amenity_input_model)
    @api.response(400, 'Invalid input')
    @api.response(403, 'Forbidden')
    @api.marshal_with(amenity_response_model)
    @admin_required
    def put(self, amenity_id):
        """Update amenity details (admin only)"""
        data = api.payload
        try:
            amenity = hbnb_facade.get_amenity(amenity_id)
            if not amenity:
                abort(404, 'Amenity not found')

            # Name uniqueness check (if name is being changed)
            if 'name' in data and data['name'] != amenity['name']:
                if hbnb_facade.get_amenity_by_name(data['name']):
                    abort(400, 'Amenity with this name already exists')

            updated_amenity = hbnb_facade.update_amenity(amenity_id, data)
            return updated_amenity, 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))

    @api.doc('delete_amenity', security='apikey')
    @api.response(204, 'Amenity deleted')
    @api.response(403, 'Forbidden')
    @api.response(409, 'Amenity in use')
    @admin_required
    def delete(self, amenity_id):
        """Delete amenity (admin only)"""
        try:
            amenity = hbnb_facade.get_amenity(amenity_id)
            if not amenity:
                abort(404, 'Amenity not found')

            # Check if amenity is being used by any places
            if hbnb_facade.is_amenity_in_use(amenity_id):
                abort(409, 'Cannot delete - amenity is in use by one or more places')

            hbnb_facade.delete_amenity(amenity_id)
            return '', 204
        except Exception as e:
            abort(500, str(e))

@api.route('/<string:amenity_id>/places')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class AmenityPlaces(Resource):
    @api.doc('get_places_with_amenity')
    @api.marshal_list_with(api.model('PlaceReference', {
        'id': fields.String,
        'title': fields.String,
        'price': fields.Float
    }))
    def get(self, amenity_id):
        """Get all places that have this amenity (public)"""
        try:
            amenity = hbnb_facade.get_amenity(amenity_id)
            if not amenity:
                abort(404, 'Amenity not found')

            places = hbnb_facade.get_places_with_amenity(amenity_id)
            return places, 200
        except Exception as e:
            abort(500, str(e))
