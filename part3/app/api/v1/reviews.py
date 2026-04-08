from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

ns = Namespace('reviews', description='Review operations')

review_model = ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@ns.route('/')
class ReviewList(Resource):
    @ns.expect(review_model)
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data')
    @ns.doc(security='Bearer')
    @jwt_required()
    def post(self):

        current_user_id = get_jwt_identity()
        try:
            review_data = ns.payload
            place = facade.get_place(review_data["place_id"])
            if place.owner_id == current_user_id:
                return {"error": "You cannot review your own place."}, 400

            existing_review = facade.get_review_by_user_and_place(
                current_user_id, review_data["place_id"])
            if existing_review:
                return {"error": "You have already reviewed this place."}, 400
            review_data["user_id"] = current_user_id

            
            if not (1 <= review_data['rating'] <= 5):
                return {'error': 'Rating must be between 1 and 5'}, 400

            
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500

    @ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        
        try:
            reviews = facade.get_all_reviews()
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                }
                for review in reviews
            ], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500


@ns.route('/<review_id>')
class ReviewResource(Resource):
    @ns.response(200, 'Review details retrieved successfully')
    @ns.response(404, 'Review not found')
    def get(self, review_id):
       
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    @ns.expect(review_model)
    @ns.response(200, 'Review updated successfully')
    @ns.response(404, 'Review not found')
    @ns.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
     
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {"error": "You can only update your own reviews"}, 403

        try:
            review_data = ns.payload

            if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
                return {'error': 'Rating must be between 1 and 5'}, 400

            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404

            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    @ns.response(200, 'Review deleted successfully')
    @ns.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        
        if review.user_id != current_user_id:
            return {"error": "You can only delete your own reviews"}, 403

        try:
            success = facade.delete_review(review_id)
            if not success:
                return {'error': 'Review not found'}, 404

            return {'message': 'Review deleted successfully'}, 200
        except Exception:
            return {'error': 'Internal server error'}, 500


@ns.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @ns.response(200, 'List of reviews for the place retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
       
        try:
            
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                }
                for review in reviews
            ], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500