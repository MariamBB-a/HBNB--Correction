from app.models.base_model import BaseModel
import re


class User(BaseModel):
    # Class-level set to track unique emails
    _emails = set()

    def __init__(self, first_name, last_name, email, password,
                 is_admin=False, is_owner=False, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Validate first_name
        if not first_name or not first_name.strip():
            raise ValueError("first_name is required")
        if len(first_name.strip()) > 50:
            raise ValueError("first_name cannot exceed 50 characters")
        self.first_name = first_name.strip()

        # Validate last_name
        if not last_name or not last_name.strip():
            raise ValueError("last_name is required")
        if len(last_name.strip()) > 50:
            raise ValueError("last_name cannot exceed 50 characters")
        self.last_name = last_name.strip()

        # Validate email
        if not email or not email.strip():
            raise ValueError("email is required")
        email = email.strip()
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            raise ValueError("invalid email format")
        if email in User._emails:
            raise ValueError("email must be unique")
        self.email = email
        User._emails.add(email)

        # Validate password
        if not password or not password.strip():
            raise ValueError("password is required")
        self.password = password.strip()

        # Admin and owner flags
        self.is_admin = bool(is_admin)
        self.is_owner = bool(is_owner)
