from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def run_tests():
    user = User("John", "Doe", "john@example.com")
    place = Place("House", "Nice house", 100, 10.0, 20.0, user)
    review = Review("Great!", 5, place, user)
    amenity = Amenity("WiFi")

    place.add_review(review)
    place.add_amenity(amenity)

    print("All tests passed!")


run_tests()
