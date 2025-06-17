from flask_restx import Namespace, Resource, fields

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review created')
    @api.response(400, 'Invalid input')
    def post(self):
        """Create a new review"""
        return {'message': 'Not implemented yet'}, 501

    @api.response(200, 'List of reviews retrieved')
    def get(self):
        """List all reviews"""
        return {'message': 'Not implemented yet'}, 501


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        return {'message': 'Not implemented yet'}, 501

    @api.expect(review_model)
    @api.response(200, 'Review updated')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update review by ID"""
        return {'message': 'Not implemented yet'}, 501

    @api.response(200, 'Review deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review by ID"""
        return {'message': 'Not implemented yet'}, 501


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for place retrieved')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """List all reviews for a specific place"""
        return {'message': 'Not implemented yet'}, 501
