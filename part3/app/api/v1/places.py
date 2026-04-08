#!/usr/bin/python3
"""Place API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

ns = Namespace('places', description='Place operations')

amenity_model = ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


place_model = ns.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner (automatically set to current user)'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@ns.route('/')
class PlaceList(Resource):
    @ns.expect(place_model)
    @ns.response(201, 'Place successfully created')
    @ns.response(400, 'Invalid input data')
    @ns.doc(security='Bearer')
    @jwt_required()
    def post(self):
        
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {"error": "Unauthorized"}, 403

        data = ns.payload
        
        data["owner_id"] = current_user_id

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @ns.response(200, 'List of places retrieved successfully')
    def get(self):
    
        try:
            all_place = facade.get_all_places()
            return [place.to_dict() for place in all_place], 200
        except Exception:
            return {"error": "An unexpected error occurred"}, 500


@ns.route('/<place_id>')
class PlaceResource(Resource):
    @ns.response(200, 'Place details retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
         
        try:
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            result = place.to_dict()
            result["owner"] = place.owner.to_dict()
            result["amenities"] = [amenities.to_dict() for amenities in place.amenities]
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @ns.expect(place_model)
    @ns.response(200, 'Place updated successfully')
    @ns.response(404, 'Place not found')
    @ns.response(400, 'Invalid input data')
    @ns.doc(security='Bearer')
    @jwt_required()
    def put(self, place_id):
       
        data = ns.payload
        current_user_id = get_jwt_identity()

        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not current_user_id:
            return {"error": "Unauthorized"}, 403

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if 'owner_id' in data and data['owner_id'] != place.owner_id:
            return {"error": "You cannot modify the owner of a place"}, 400

        
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "You can only update your own places"}, 403

        try:
           update_place = facade.update_place(place_id, data)
           return update_place.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
    
    @ns.response(204, 'Place deleted successfully')
    @ns.response(404, 'Place not found')
    @ns.response(403, 'Unauthorized action')
    @ns.doc(security='Bearer')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place - Owner or Admin only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin and place.owner_id != current_user_id:
            return {"error": "You can only delete your own places"}, 403

        facade.delete_place(place_id)
        return '', 204 