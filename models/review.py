from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, user, place, comment, rating, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Validate user
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")
        self.user = user

        # Validate place
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        self.place = place

        # Validate comment
        if not comment or not comment.strip():
            raise ValueError("comment is required")
        self.comment = comment.strip()

        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self.rating = rating

    def save(self):
        """Update updated_at timestamp"""
        super().save()

    def to_dict(self):
        """Return dictionary representation for JSON or storage"""
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user.id,
            'place_id': self.place.id,
            'comment': self.comment,
            'rating': self.rating
        })
        return base_dict
