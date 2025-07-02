from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade as hbnb_facade

api = Namespace('reviews', description='Review operations')

review_input_model = api.model(
    'ReviewInput',
    {
        'text': fields.String(required=True, description='Review content'),
        'rating': fields.Integer(required=True, description='Rating (1-5)'),
        'place_id': fields.String(required=True, description='Place ID'),
    }
)

review_response_model = api.model(
    'ReviewResponse',
    {
        'id': fields.String(description='Review ID'),
        'text': fields.String(description='Review content'),
        'rating': fields.Integer(description='Rating (1-5)'),
        'user_id': fields.String(description='User ID'),
        'place_id': fields.String(description='Place ID'),
        'created_at': fields.DateTime(description='Creation date'),
        'updated_at': fields.DateTime(description='Last update date'),
    }
)

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """List all reviews (public)"""
        try:
            return hbnb_facade.get_all_reviews(), 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('create_review', security='apikey')
    @api.expect(review_input_model)
    @api.response(400, 'Invalid input')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User or Place not found')
    @api.response(409, 'Already reviewed')
    @api.response(201, 'Review created')
    @api.marshal_with(review_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review (authenticated)"""
        current_user = get_jwt_identity()
        data = api.payload

        if not data.get('text'):
            abort(400, 'Review text is required')

        if not isinstance(data.get('rating'), int) or not (1 <= data['rating'] <= 5):
            abort(400, 'Rating must be an integer between 1 and 5')

        try:
            # Check if place exists
            place = hbnb_facade.get_place(data['place_id'])
            if not place:
                abort(404, 'Place not found')
            
            # Check if user is trying to review their own place
            if place['owner_id'] == current_user:
                abort(403, 'Cannot review your own place')
            
            # Check for existing review by this user for this place
            existing_reviews = hbnb_facade.get_reviews_by_place(data['place_id'])
            for review in existing_reviews:
                if review['user_id'] == current_user:
                    abort(409, 'You have already reviewed this place')
            
            # Add the current user as the reviewer
            data['user_id'] = current_user
            review = hbnb_facade.create_review(data)
            return review, 201
        except ValueError as e:
            abort(400, str(e))
        except LookupError as e:
            abort(404, str(e))
        except Exception as e:
            abort(500, str(e))

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """Get review by ID (public)"""
        try:
            review = hbnb_facade.get_review(review_id)
            if not review:
                abort(404, 'Review not found')
            return review, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('update_review', security='apikey')
    @api.expect(review_input_model)
    @api.response(400, 'Invalid input')
    @api.response(403, 'Forbidden')
    @api.marshal_with(review_response_model)
    @jwt_required()
    def put(self, review_id):
        """Update review details (reviewer only)"""
        current_user = get_jwt_identity()

        if 'rating' in api.payload and (not isinstance(api.payload['rating'], int) or not (1 <= api.payload['rating'] <= 5)):
            abort(400, 'Rating must be an integer between 1 and 5')

        try:
            review = hbnb_facade.get_review(review_id)
            if not review:
                abort(404, 'Review not found')
            
            if review['user_id'] != current_user:
                abort(403, 'Only the reviewer can update this review')
            
            # Prevent changing place_id or user_id
            data = api.payload
            if 'place_id' in data:
                del data['place_id']
            if 'user_id' in data:
                del data['user_id']
            
            review = hbnb_facade.update_review(review_id, data)
            return review, 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))

    @api.doc('delete_review', security='apikey')
    @api.response(204, 'Review deleted')
    @api.response(403, 'Forbidden')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (reviewer or admin only)"""
        current_user = get_jwt_identity()
        
        try:
            review = hbnb_facade.get_review(review_id)
            if not review:
                abort(404, 'Review not found')
            
            # In a real app, you might want to check for admin role here too
            if review['user_id'] != current_user:
                abort(403, 'Only the reviewer can delete this review')
            
            success = hbnb_facade.delete_review(review_id)
            if not success:
                abort(404, 'Review not found')
            return '', 204
        except Exception as e:
            abort(500, str(e))

@api.route('/place/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_response_model)
    def get(self, place_id):
        """Get all reviews for a specific place (public)"""
        try:
            reviews = hbnb_facade.get_reviews_by_place(place_id)
            return reviews, 200
        except LookupError as e:
            abort(404, str(e))
        except Exception as e:
            abort(500, str(e))
