from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace("places", description="Places operations")
facade = HBnBFacade()

place_model = api.model("Place", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True, max_length=100),
    "description": fields.String(default=""),
    "price": fields.Float(default=0.0),
    "latitude": fields.Float(default=0.0),
    "longitude": fields.Float(default=0.0),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.String, default=[])
})


@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places]

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new place"""
        data = api.payload

        # Validate required fields
        if not data.get("title") or not data.get("owner_id"):
            api.abort(400, "Title and owner_id are required")

        # Validate numeric attributes
        if data.get("price", 0.0) < 0:
            api.abort(400, "Price must be non-negative")
        if not (-90 <= data.get("latitude", 0.0) <= 90):
            api.abort(400, "Latitude must be between -90 and 90")
        if not (-180 <= data.get("longitude", 0.0) <= 180):
            api.abort(400, "Longitude must be between -180 and 180")

        # Validate owner exists
        owner = facade.get_user(data["owner_id"])
        if not owner:
            api.abort(404, "Owner not found")

        # Validate amenities exist
        amenity_ids = data.get("amenities", [])
        for a_id in amenity_ids:
            if not facade.get_amenity(a_id):
                api.abort(404, f"Amenity {a_id} not found")

        try:
            place = facade.create_place(data)
        except ValueError as e:
            api.abort(400, str(e))

        return place.to_dict(), 201


@api.route("/<string:place_id>")
class PlaceItem(Resource):
    @api.marshal_with(place_model)
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Retrieve a place by ID, including owner and amenities"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()

    @api.expect(place_model)
    @api.marshal_with(place_model)
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        data = api.payload

        # Validate numeric attributes if present
        if "price" in data and data["price"] < 0:
            api.abort(400, "Price must be non-negative")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            api.abort(400, "Latitude must be between -90 and 90")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            api.abort(400, "Longitude must be between -180 and 180")

        # Validate owner if updating
        if "owner_id" in data:
            if not facade.get_user(data["owner_id"]):
                api.abort(404, "Owner not found")

        # Validate amenities if updating
        if "amenities" in data:
            for a_id in data["amenities"]:
                if not facade.get_amenity(a_id):
                    api.abort(404, f"Amenity {a_id} not found")

        try:
            updated = facade.update_place(place_id, data)
        except ValueError as e:
            api.abort(400, str(e))

        return updated.to_dict()
