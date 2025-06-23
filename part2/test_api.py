import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['email'], "john.doe@example.com")
        self.user_id = data['id']

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Invalid",
            "last_name": "Email",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "place.owner@example.com"
        })
        self.user_id = user_response.get_json()['id']

    def test_create_place_valid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": 200,
            "latitude": 24.0,
            "longitude": 40.0,
            "user_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], "Beach House")

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cheap Place",
            "price": -50,
            "latitude": 24.0,
            "longitude": 40.0,
            "user_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)


class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_valid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], "WiFi")

    def test_create_amenity_empty_name(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Review",
            "last_name": "Tester",
            "email": "review.tester@example.com"
        })
        self.user_id = user_response.get_json()['id']

        # create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Place",
            "price": 150,
            "latitude": 30.0,
            "longitude": 50.0,
            "user_id": self.user_id
        })
        self.place_id = place_response.get_json()['id']

    def test_create_review_valid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad rating",
            "rating": 8,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['email'], "john.doe@example.com")
        self.user_id = data['id']

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Invalid",
            "last_name": "Email",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "place.owner@example.com"
        })
        self.user_id = user_response.get_json()['id']

    def test_create_place_valid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": 200,
            "latitude": 24.0,
            "longitude": 40.0,
            "user_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], "Beach House")

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cheap Place",
            "price": -50,
            "latitude": 24.0,
            "longitude": 40.0,
            "user_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)


class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_valid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], "WiFi")

    def test_create_amenity_empty_name(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Review",
            "last_name": "Tester",
            "email": "review.tester@example.com"
        })
        self.user_id = user_response.get_json()['id']

        # create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Place",
            "price": 150,
            "latitude": 30.0,
            "longitude": 50.0,
            "user_id": self.user_id
        })
        self.place_id = place_response.get_json()['id']

    def test_create_review_valid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad rating",
            "rating": 8,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
