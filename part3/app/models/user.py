#!/usr/bin/python3
import re
from app.models.base_model import BaseModel
from hbnb.app.extensions import db
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required (max 50 chars)")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required (max 50 chars)")

        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not email or not re.match(email_regex, email):
            raise ValueError("A valid email address is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)