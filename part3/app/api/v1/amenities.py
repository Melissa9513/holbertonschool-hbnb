#!/usr/bin/python3
"""Amenity API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


ns = Namespace('amenities', description='Amenity operations')


amenity_input_model = ns.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_output_model = ns.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

@ns.route('/')
class AmenityList(Resource):
    @ns.expect(amenity_input_model)
    @ns.marshal_with(amenity_output_model, code=201)
    @ns.response(201, 'Amenity successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        
        amenity_data = ns.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    @ns.marshal_list_with(amenity_output_model)
    @ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
  
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@ns.route('/<amenity_id>')
class AmenityResource(Resource):
    @ns.marshal_with(amenity_output_model)
    @ns.response(200, 'Amenity details retrieved successfully')
    @ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
 
        get_amenity = facade.get_amenity(amenity_id)
        if not get_amenity:
            return {"error": "Amenity not found"}, 404
        return get_amenity.to_dict(), 200

    @ns.expect(amenity_input_model)
    @ns.marshal_with(amenity_output_model)
    @ns.response(200, 'Amenity updated successfully')
    @ns.response(404, 'Amenity not found')
    @ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        amenity_data = ns.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return updated_amenity.to_dict(), 200