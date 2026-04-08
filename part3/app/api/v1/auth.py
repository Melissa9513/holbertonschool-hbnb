from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

ns = Namespace('auth', description='Authentication operations')


login_model = ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = ns.payload

        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

        return {'access_token': access_token}, 200