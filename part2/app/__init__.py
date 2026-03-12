#!/usr/bin/python3
"""
Main application factory and API initialization.
"""
from flask import Flask
from flask_restx import Api

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    # Initialize the API with basic metadata and Swagger documentation path
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API Documentation',
              doc='/api/v1/' # URL for the Swagger UI
    )
    #Register the namespaces HERE, after 'api' is defined
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    return app
