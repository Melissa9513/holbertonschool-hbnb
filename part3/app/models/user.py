#!/usr/bin/python3
import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required (max 50 chars)")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required (max 50 chars)")

        email_regex = r"[^@]+@[^@]+.[^@]+"
        if not email or not re.match(email_regex, email):
            raise ValueError("A valid email address is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
