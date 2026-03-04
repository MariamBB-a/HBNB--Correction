from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

review_model = api.model("Review", {
    "id": fields.String(readonly=True),
    "user_id": fields.String(required=True, description="User who wrote the review"),
    "place_id": fields.String(required=True, description="Place being reviewed"),
    "comment": fields.String(required=True, description="Review text"),
    "rating": fields.Integer(required=True, description="Rating (1-5)", min=1, max=5)
})

# --------- List and Create Reviews ---------


@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Retrieve all reviews"""
        return [r.to_dict() for r in facade.get_all_reviews()]

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = api.payload

        # Validate user
        user = facade.get_user(data["user_id"])
        if not user:
            api.abort(404, "User not found")

        # Validate place
        place = facade.get_place(data["place_id"])
        if not place:
            api.abort(404, "Place not found")

        # Validate rating
        rating = data.get("rating")
        if not (1 <= rating <= 5):
            api.abort(400, "Rating must be between 1 and 5")

        # Validate comment
        if not data.get("comment"):
            api.abort(400, "Comment is required")

        review_data = {
            "user_id": data["user_id"],
            "place_id": data["place_id"],
            "comment": data["comment"],
            "rating": data["rating"]
        }

        review = facade.create_review(review_data)
        return review.to_dict(), 201


# --------- Review by ID ---------
@api.route("/<string:review_id>")
class ReviewItem(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict()

    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        data = api.payload

        # Validate rating
        if "rating" in data and not (1 <= data["rating"] <= 5):
            api.abort(400, "Rating must be between 1 and 5")
        # Validate comment
        if "comment" in data and not data["comment"]:
            api.abort(400, "Comment cannot be empty")

        updated_review = facade.update_review(review_id, data)
        return updated_review.to_dict(), 200

    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return {"message": "Review deleted"}, 200


# --------- Reviews by Place ---------
@api.route("/place/<string:place_id>")
class ReviewsByPlace(Resource):
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews]
