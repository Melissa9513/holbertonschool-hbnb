#!/usr/bin/python3
"""Review module"""
from app.models.base_model import BaseModel
from app import db
class Review(BaseModel):
    """Review entity for user feedback on places."""

    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    def __init__(self, **kwargs):
        """Initialize Review with rating and existence validation."""
    
        text = kwargs.get('text')
        rating = kwargs.get('rating')

        if not text:
            raise ValueError("Review text is required")
        
        if rating is None or not (1 <= int(rating) <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
       
        super().__init__(**kwargs)