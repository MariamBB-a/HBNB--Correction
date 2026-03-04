from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Validate name
        if not name or not name.strip():
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("name must be 50 characters or less")

        self.name = name.strip()
        self.description = description.strip() if description else ""
