from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace("users", description="User operations")
facade = HBnBFacade()

user_model = api.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True, description="First name of the user"),
    "last_name": fields.String(required=True, description="Last name of the user"),
    "email": fields.String(required=True, description="Email of the user"),
    "password": fields.String(required=True, description="User password")
})


@api.route("/")
class UsersList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve all users"""
        return [u.to_dict() for u in facade.get_all_users()]

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload

        # Validation
        if not data.get("first_name") or not data.get("last_name") or not data.get("email") or not data.get("password"):
            api.abort(
                400, "All fields (first_name, last_name, email, password) are required")

        # Email uniqueness
        existing_user = facade.get_user_by_email(data["email"])
        if existing_user:
            api.abort(400, "Email already registered")

        try:
            user = facade.create_user(data)
        except ValueError as e:
            api.abort(400, str(e))

        return user.to_dict(), 201


@api.route("/<string:user_id>")
class UserItem(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update an existing user"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        data = api.payload

        # Basic validation
        if "email" in data:
            existing_user = facade.get_user_by_email(data["email"])
            if existing_user and existing_user.id != user_id:
                api.abort(400, "Email already registered")

        try:
            updated_user = facade.update_user(user_id, data)
        except ValueError as e:
            api.abort(400, str(e))

        return updated_user.to_dict(), 200
