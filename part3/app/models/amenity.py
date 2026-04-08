#!/usr/bin/python3
"""Amenity module"""
from app.models.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    """Amenity entity (e.g., Wi-Fi, Parking)."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """Initialize Amenity with name validation."""
        super().__init__()
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string.")
        elif not name.strip():
            raise ValueError("Amenity name cannot be empty.")
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required (max 50 chars)")
        self.name = name
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }