from flask_restx import Namespace, Resource, fields, abort
from app.services import facade as hbnb_facade

api = Namespace('reviews', description='Review operations')

# Input Model
review_input_model = api.model(
    'ReviewInput',
    {
        'text': fields.String(required=True, description='Review content'),
        'rating': fields.Integer(required=True, description='Rating (1-5)'),
        'user_id': fields.String(required=True, description='User ID'),
        'place_id': fields.String(required=True, description='Place ID'),
    }
)

# Response Model
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
        """List all reviews"""
        try:
            return hbnb_facade.get_all_reviews(), 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('create_review')
    @api.expect(review_input_model)
    @api.response(400, 'Invalid input')
    @api.response(404, 'User or Place not found')
    @api.response(201, 'Review created')
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """Create a new review"""
        data = api.payload

        if not data.get('text'):
            abort(400, 'Review text is required')

        if not isinstance(data.get('rating'), int) or not (1 <= data['rating'] <= 5):
            abort(400, 'Rating must be an integer between 1 and 5')

        try:
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
        """Get review by ID"""
        try:
            review = hbnb_facade.get_review(review_id)
            if not review:
                abort(404, 'Review not found')
            return review, 200
        except Exception as e:
            abort(500, str(e))

    @api.doc('update_review')
    @api.expect(review_input_model)
    @api.response(400, 'Invalid input')
    @api.marshal_with(review_response_model)
    def put(self, review_id):
        """Update review details"""
        data = api.payload

        if 'rating' in data and (not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5)):
            abort(400, 'Rating must be an integer between 1 and 5')

        try:
            review = hbnb_facade.update_review(review_id, data)
            if not review:
                abort(404, 'Review not found')
            return review, 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, str(e))

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review"""
        try:
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
        """Get all reviews for a specific place"""
        try:
            reviews = hbnb_facade.get_reviews_by_place(place_id)
            return reviews, 200
        except LookupError as e:
            abort(404, str(e))
        except Exception as e:
            abort(500, str(e))

