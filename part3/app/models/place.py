#!/usr/bin/python3
"""Place module"""
from app.models.base_model import BaseModel
from app import db

class Place(BaseModel):
    """Place entity representing property listings."""

    def __init__(self, title, price, latitude, longitude, owner, amenity , description=None):
        """Initialize Place with strict coordinate and price validation."""
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Title is required (max 100 chars)")
        if price <= 0:
            raise ValueError("Price must be a positive value")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        if owner is None:
            raise ValueError("A place must have a valid owner")

        self.title = title
        self.description = description # Optional
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner  # User instance
        self.amenities = [] # List of Amenity instances
        self.reviews = []   # List of Review instances

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
            self.reviews.append(review)
