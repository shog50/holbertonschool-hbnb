from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade as hbnb_facade
from app.services.auth import admin_required

api = Namespace('places', description='Place operations')

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Geographic coordinate'),
    'longitude': fields.Float(description='Geographic coordinate'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Geographic coordinate'),
    'longitude': fields.Float(description='Geographic coordinate'),
    'owner_id': fields.String(description='Owner ID'),
    'amenities': fields.List(fields.Nested(api.model('PlaceAmenity', {
        'id': fields.String,
        'name': fields.String
    }))),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model)
    def get(self):
        """List all places (public)"""
        try:
            return hbnb_facade.get_all_places(), 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('create_place', security='apikey')
    @api.expect(place_input_model)
    @api.response(400, 'Invalid input')
    @api.response(201, 'Place created')
    @api.marshal_with(place_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place (authenticated)"""
        current_user = get_jwt_identity()
        data = api.payload
        
        # Basic validation
        if not data.get('title'):
            abort(400, 'Title is required')
        if not isinstance(data.get('price'), (int, float)) or data['price'] <= 0:
            abort(400, 'Price must be a positive number')

        # Set the owner to the current user
        data['owner_id'] = current_user['id']

        try:
            place = hbnb_facade.create_place(data)
            return place, 201
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """Get place by ID (public)"""
        try:
            place = hbnb_facade.get_place(place_id)
            if not place:
                abort(404, 'Place not found')
            return place, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('update_place', security='apikey')
    @api.expect(place_input_model)
    @api.response(400, 'Invalid input')
    @api.response(403, 'Forbidden')
    @api.marshal_with(place_response_model)
    @jwt_required()
    def put(self, place_id):
        """Update place details (owner or admin)"""
        current_user = get_jwt_identity()
        
        try:
            place = hbnb_facade.get_place(place_id)
            if not place:
                abort(404, 'Place not found')
            
            # Check if current user is owner or admin
            is_admin = current_user.get('is_admin', False)
            if place['owner_id'] != current_user['id'] and not is_admin:
                abort(403, 'Only the owner or admin can update this place')

            data = api.payload
            # Price validation if provided
            if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
                abort(400, 'Price must be a positive number')

            # Prevent owner_id change unless admin
            if 'owner_id' in data and not is_admin:
                del data['owner_id']

            place = hbnb_facade.update_place(place_id, data)
            return place, 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))

    @api.doc('delete_place', security='apikey')
    @api.response(204, 'Place deleted')
    @api.response(403, 'Forbidden')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (owner or admin)"""
        current_user = get_jwt_identity()
        
        try:
            place = hbnb_facade.get_place(place_id)
            if not place:
                abort(404, 'Place not found')
            
            # Check if current user is owner or admin
            is_admin = current_user.get('is_admin', False)
            if place['owner_id'] != current_user['id'] and not is_admin:
                abort(403, 'Only the owner or admin can delete this place')

            hbnb_facade.delete_place(place_id)
            return '', 204
        except Exception as e:
            abort(500, str(e))

@api.route('/<string:place_id>/transfer')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
@api.response(403, 'Forbidden')
class PlaceTransfer(Resource):
    @api.doc('transfer_ownership', security='apikey')
    @api.expect(api.model('TransferInput', {
        'new_owner_id': fields.String(required=True)
    }))
    @api.marshal_with(place_response_model)
    @admin_required
    def put(self, place_id):
        """Transfer place ownership (admin only)"""
        try:
            place = hbnb_facade.get_place(place_id)
            if not place:
                abort(404, 'Place not found')
            
            new_owner_id = api.payload['new_owner_id']
            if not hbnb_facade.user_repo.get(new_owner_id):
                abort(400, 'New owner not found')
            
            updated_place = hbnb_facade.update_place(place_id, {'owner_id': new_owner_id})
            return updated_place, 200
        except Exception as e:
            abort(500, str(e))
