from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace("places", description="Place operations")
facade = HBnBFacade()

place_model = api.model("Place", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(default="", description="Description of the place"),
    "price": fields.Float(default=0.0, description="Price of the place"),
    "latitude": fields.Float(default=0.0, description="Latitude of the place (-90 to 90)"),
    "longitude": fields.Float(default=0.0, description="Longitude of the place (-180 to 180)"),
    "owner_id": fields.String(required=True, description="User ID of the owner"),
    "amenities": fields.List(fields.String, default=[], description="List of Amenity IDs")
})


@api.route("/")
class PlacesList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """Retrieve all places"""
        return [p.to_dict() for p in facade.get_all_places()]

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = api.payload

        # Required fields
        required = ["title", "owner_id"]
        for field in required:
            if not data.get(field):
                api.abort(400, f"{field} is required")

        # Validate owner exists
        owner = facade.get_user(data["owner_id"])
        if not owner:
            api.abort(404, "Owner not found")

        # Validate price
        price = data.get("price", 0.0)
        if price < 0:
            api.abort(400, "Price cannot be negative")

        # Validate latitude and longitude
        lat = data.get("latitude", 0.0)
        lon = data.get("longitude", 0.0)
        if not (-90 <= lat <= 90):
            api.abort(400, "Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            api.abort(400, "Longitude must be between -180 and 180")

        # Validate amenities
        amenities_ids = data.get("amenities", [])
        amenities = []
        for a_id in amenities_ids:
            amenity = facade.get_amenity(a_id)
            if not amenity:
                api.abort(404, f"Amenity {a_id} not found")
            amenities.append(amenity)

        # Create place
        place_data = {
            "title": data["title"],
            "description": data.get("description", ""),
            "price": price,
            "latitude": lat,
            "longitude": lon,
            "owner_id": data["owner_id"],
            "amenities": amenities
        }

        place = facade.create_place(place_data)
        return place.to_dict(), 201


@api.route("/<string:place_id>")
class PlaceItem(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Retrieve a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update an existing place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        data = api.payload

        # Validate attributes if present
        if "price" in data and data["price"] < 0:
            api.abort(400, "Price cannot be negative")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            api.abort(400, "Latitude must be between -90 and 90")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            api.abort(400, "Longitude must be between -180 and 180")
        if "owner_id" in data:
            owner = facade.get_user(data["owner_id"])
            if not owner:
                api.abort(404, "Owner not found")
        if "amenities" in data:
            amenities = []
            for a_id in data["amenities"]:
                amenity = facade.get_amenity(a_id)
                if not amenity:
                    api.abort(404, f"Amenity {a_id} not found")
                amenities.append(amenity)
            data["amenities"] = amenities

        updated_place = facade.update_place(place_id, data)
        return updated_place.to_dict(), 200
