from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description="", price=0.0,
                 latitude=0.0, longitude=0.0, owner=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Validate title
        if not title or not title.strip():
            raise ValueError("title is required")
        if len(title.strip()) > 100:
            raise ValueError("title must be <= 100 characters")
        self.title = title.strip()

        # Description is optional
        self.description = description.strip() if description else ""

        # Validate price
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a positive number")
        self.price = float(price)

        # Validate latitude
        if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90 and 90")
        self.latitude = float(latitude)

        # Validate longitude
        if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180 and 180")
        self.longitude = float(longitude)

        # Validate owner
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")
        self.owner = owner

        # Relationships
        self.reviews = []   # List of Review instances
        self.amenities = []  # List of Amenity instances

    # Methods to manage relationships
    def add_review(self, review):
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)
        self.save()  # Update updated_at

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
        self.save()  # Update updated_at
