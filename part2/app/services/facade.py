#!/usr/bin/python3
"""
Facade module for handling business logic and repository interactions.
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def init(self):
        """Initialize repositories"""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create and return a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update and return a user"""
        user = self.get_user(user_id)
        if not user:
            return None

        # Update object attributes (keeps business object consistent)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.email = user_data['email']

        # Persist update in repository
        self.user_repo.update(user_id, user_data)
        return user 
