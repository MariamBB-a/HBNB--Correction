from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # -------- USERS --------
    def create_user(self, data):
        # Check email uniqueness
        if self.user_repo.get_by_attribute("email", data["email"]):
            raise ValueError("Email already registered")
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "email" in data:
            # Check uniqueness for updated email
            existing = self.user_repo.get_by_attribute("email", data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    def delete_user(self, user_id):
        self.user_repo.delete(user_id)

    # -------- PLACES --------
    def create_place(self, data):
        # Validate owner exists
        owner = self.get_user(data["owner"])
        if not owner:
            raise ValueError("Owner not found")

        # Validate amenities exist
        amenities_ids = data.get("amenities", [])
        for amenity_id in amenities_ids:
            if not self.amenity_repo.get(amenity_id):
                raise ValueError(f"Amenity {amenity_id} not found")

        # Validate numeric fields
        price = data.get("price", 0.0)
        lat = data.get("latitude", 0.0)
        lng = data.get("longitude", 0.0)
        if price < 0:
            raise ValueError("Price cannot be negative")
        if not -90 <= lat <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= lng <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        place = Place(**data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # Validate updates
        if "price" in data and data["price"] < 0:
            raise ValueError("Price cannot be negative")
        if "latitude" in data and not -90 <= data["latitude"] <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if "longitude" in data and not -180 <= data["longitude"] <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        if "owner" in data and not self.get_user(data["owner"]):
            raise ValueError("Owner not found")
        # Validate amenities
        if "amenities" in data:
            for amenity_id in data["amenities"]:
                if not self.amenity_repo.get(amenity_id):
                    raise ValueError(f"Amenity {amenity_id} not found")

        self.place_repo.update(place_id, data)
        return self.place_repo.get(place_id)

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    # -------- AMENITIES --------
    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, data)
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)

    # -------- REVIEWS --------
    def create_review(self, data):
        # Validate related objects
        if not self.get_user(data["user_id"]):
            raise ValueError("User not found")
        if not self.get_place(data["place_id"]):
            raise ValueError("Place not found")
        if "rating" not in data or not (1 <= data["rating"] <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if "comment" not in data or not data["comment"]:
            raise ValueError("Comment is required")

        review = Review(**data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute("place_id", place_id)

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if "rating" in data and not (1 <= data["rating"] <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if "comment" in data and not data["comment"]:
            raise ValueError("Comment cannot be empty")
        self.review_repo.update(review_id, data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
