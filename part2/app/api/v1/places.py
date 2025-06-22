from flask_restx import Namespace, Resource, fields, abort
from app.services import facade as hbnb_facade

api = Namespace('places', description='Place operations')

# Simplified Models
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Geographic coordinate'),
    'longitude': fields.Float(description='Geographic coordinate'),
    'owner_id': fields.String(required=True, description='Owner ID'),
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
    'amenities': fields.List(fields.Nested(
        api.model('PlaceAmenity', {
            'id': fields.String,
            'name': fields.String
        })
    )
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model)
    def get(self):
        """List all places"""
        try:
            return hbnb_facade.get_all_places(), 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('create_place')
    @api.expect(place_input_model)
    @api.response(400, 'Invalid input')
    @api.response(201, 'Place created')
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """Create a new place"""
        data = api.payload
        
        # Basic validation
        if not data.get('title'):
            abort(400, 'Title is required')
        if not isinstance(data.get('price'), (int, float)) or data['price'] <= 0:
            abort(400, 'Price must be a positive number')

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
        """Get place by ID"""
        try:
            place = hbnb_facade.get_place(place_id)
            if not place:
                abort(404, 'Place not found')
            return place, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('update_place')
    @api.expect(place_input_model)
    @api.response(400, 'Invalid input')
    @api.marshal_with(place_response_model)
    def put(self, place_id):
        """Update place details"""
        data = api.payload
        
        # Price validation if provided
        if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] <= 0:
            abort(400, 'Price must be a positive number')

        try:
            place = hbnb_facade.update_place(place_id, data)
            if not place:
                abort(404, 'Place not found')
            return place, 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))
