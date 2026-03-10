#!/usr/bin/python3
"""
BaseModel module
Provides the base class for all entities in the HBnB application.
"""
import uuid
from datetime import datetime

class BaseModel:
    """Base class that defines all common attributes/methods for other classes."""

    def __init__(self):
        """Initialize a new base model instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes based on a dictionary of new values."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
