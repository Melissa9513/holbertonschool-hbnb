#!/usr/bin/python3
"""Amenity module"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity entity (e.g., Wi-Fi, Parking)."""

    def __init__(self, name):
        """Initialize Amenity with name validation."""
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required (max 50 chars)")
        self.name = name
