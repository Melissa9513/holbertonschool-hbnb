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
    def __init__(self):
        """Initialize repositories"""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # -------------------------
    # Users
    # -------------------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None

        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.email = user_data['email']

        self.user_repo.update(user_id, user_data)
        return user

    # -------------------------
    # Amenities
    # -------------------------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)  # expects {"name": "..."}
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # -------------------------
    # Places
    # -------------------------
    def create_place(self, place_data):
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        data = place_data.copy()
        data.pop('owner_id', None)

        place = Place(owner=owner, **data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        place.title = place_data['title']
        place.description = place_data.get('description')
        place.price = float(place_data['price'])
        place.latitude = float(place_data['latitude'])
        place.longitude = float(place_data['longitude'])

        self.place_repo.update(place_id, place_data)
        return place

    # -------------------------
    # Reviews
    # -------------------------
    def create_review(self, review_data):
        user = self.get_user(review_data.get('user_id'))
        place = self.get_place(review_data.get('place_id'))
        if not user or not place:
            raise ValueError("Invalid User or Place ID")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)

        # Keep Place object consistent
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = int(review_data['rating'])

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
