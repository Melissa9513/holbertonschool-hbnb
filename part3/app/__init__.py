#!/usr/bin/python3
"""
Main application factory and API initialization.
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from app.api.v1.users import ns as users_ns
    from app.api.v1.amenities import ns as amenities_ns
    from app.api.v1.places import ns as places_ns
    from app.api.v1.reviews import ns as reviews_ns
    from app.api.v1.auth import ns as auth_ns
    from app.api.v1.protected import ns as protected_ns

    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter: Bearer <your_token>'
        }
    }

    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API Documentation',
              doc='/api/v1/',
              authorizations=authorizations,
              security='Bearer'
              )
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')
    
    return app