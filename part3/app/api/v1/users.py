#!/usr/bin/python3
"""User API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

user_input_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user (min 8 chars)'),
    'is_admin': fields.Boolean(required=False, description='Admin status (admin auth required if true)')
})

user_output_model = ns.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_input_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin access required to create admin users')
    @api.doc(security='Bearer')
    @jwt_required(optional=True)
    def post(self):
        """Register a new user"""
        user_data = ns.payload

        if user_data.get('is_admin', False):
            # Auth required for admin creation
            claims = get_jwt()
            if not claims or not claims.get('is_admin', False):
                return {'error': 'Admin privileges required to create admin users'}, 403

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        if 'password' not in user_data or not user_data['password']:
            return {'error': 'Password is required'}, 400
       
        try:
            new_user = facade.create_user(user_data)
            
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400
        return new_user.to_dict(), 201

   
    @api.marshal_list_with(user_output_model)
    @api.response(200, 'List of users')
    @api.response(403, 'Admin access required')
    @api.doc(security='Bearer')
    @jwt_required()
    def get(self):
      
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):

    @api.marshal_with(user_output_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
     
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict()

    
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_output_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, user_id):
    
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
 
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        
        if not is_admin and user_id != current_user_id:
            return {"error": "You can only modify your own profile"}, 403

        user_data = ns.payload

        
        if not is_admin and 'is_admin' in user_data:
            return {"error": "Only admins can modify admin status"}, 403

        
        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        
        updated_user = facade.update_user(user_id, user_data)
        return updated_user.to_dict(), 200