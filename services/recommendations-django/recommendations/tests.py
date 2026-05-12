from django.test import SimpleTestCase, RequestFactory
from .views import (
    parse_positive_int,
    top_selling_recommendations,
    user_recommendations,
    price_max_recommendations
)

import json


# =========================================================
# Tests for utility functions
# =========================================================

class ParsePositiveIntTests(SimpleTestCase):

    # Test that a valid positive integer is returned correctly
    def test_returns_valid_positive_integer(self):
        result = parse_positive_int(5)

        self.assertEqual(result, 5)
        self.assertIsInstance(result, int)

    # Test that negative numbers return None
    def test_returns_none_for_negative_number(self):
        result = parse_positive_int(-3)

        self.assertIsNone(result)

    # Test that zero returns None
    def test_returns_none_for_zero(self):
        result = parse_positive_int(0)

        self.assertIsNone(result)

    # Test that numeric strings are converted into integers
    def test_converts_numeric_string_to_integer(self):
        result = parse_positive_int("10")

        self.assertEqual(result, 10)
        self.assertIsInstance(result, int)

    # Test that invalid strings return None
    def test_returns_none_for_invalid_string(self):
        result = parse_positive_int("abc")

        self.assertIsNone(result)

    # Test that None values return None
    def test_returns_none_for_none_value(self):
        result = parse_positive_int(None)

        self.assertIsNone(result)


# =========================================================
# Tests for top selling recommendations endpoint
# =========================================================

class TopSellingRecommendationsTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Test that GET requests are rejected
    def test_returns_405_for_invalid_http_method(self):
        request = self.factory.get('/recommendations/top-selling/')

        response = top_selling_recommendations(request)

        self.assertEqual(response.status_code, 405)

    # Test that invalid JSON bodies return status 400
    def test_returns_400_for_invalid_json_body(self):
        request = self.factory.post(
            '/recommendations/top-selling/',
            data='invalid json',
            content_type='application/json'
        )

        response = top_selling_recommendations(request)

        self.assertEqual(response.status_code, 400)

    # Test that products are sorted correctly by total sales
    def test_returns_top_selling_products_correctly(self):
        body = {
            "sales": [
                {"productId": 1, "quantity": 5},
                {"productId": 2, "quantity": 2},
                {"productId": 1, "quantity": 3}
            ],
            "products": [
                {"id": 1, "name": "Laptop", "stock": 10},
                {"id": 2, "name": "Mouse", "stock": 5}
            ]
        }

        request = self.factory.post(
            '/recommendations/top-selling/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = top_selling_recommendations(request)

        data = json.loads(response.content)

        # Validate successful response
        self.assertEqual(response.status_code, 200)

        # Validate number of recommendations
        self.assertEqual(len(data['recommendations']), 2)

        # Validate first recommended product
        self.assertEqual(data['recommendations'][0]['id'], 1)

        # Validate accumulated sales amount
        self.assertEqual(data['recommendations'][0]['totalSold'], 8)

        # Validate sorting order
        self.assertGreater(
            data['recommendations'][0]['totalSold'],
            data['recommendations'][1]['totalSold']
        )


# =========================================================
# Tests for user recommendations endpoint
# =========================================================

class UserRecommendationsTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Test that missing userId returns status 400
    def test_returns_400_when_user_id_is_missing(self):
        body = {
            "sales": [],
            "products": []
        }

        request = self.factory.post(
            '/recommendations/user/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = user_recommendations(request)

        self.assertEqual(response.status_code, 400)

    # Test that invalid userId values return status 400
    def test_returns_400_when_user_id_is_invalid(self):
        body = {
            "userId": -1,
            "sales": [],
            "products": []
        }

        request = self.factory.post(
            '/recommendations/user/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = user_recommendations(request)

        self.assertEqual(response.status_code, 400)

    # Test that recommendations are generated correctly for a user
    def test_returns_recommendations_for_user(self):
        body = {
            "userId": 1,
            "sales": [
                {"userId": 1, "productId": 1},
                {"userId": 1, "productId": 2},
                {"userId": 2, "productId": 3}
            ],
            "products": [
                {"id": 1, "name": "Laptop", "stock": 10},
                {"id": 2, "name": "Mouse", "stock": 5},
                {"id": 3, "name": "Keyboard", "stock": 8}
            ]
        }

        request = self.factory.post(
            '/recommendations/user/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = user_recommendations(request)

        data = json.loads(response.content)

        # Validate successful response
        self.assertEqual(response.status_code, 200)

        # Validate number of recommendations
        self.assertEqual(len(data['recommendations']), 2)

        # Validate recommended products
        self.assertEqual(data['recommendations'][0]['id'], 1)
        self.assertEqual(data['recommendations'][1]['id'], 2)

    # Test that products with zero stock are excluded
    def test_does_not_return_products_with_zero_stock(self):
        body = {
            "userId": 1,
            "sales": [
                {"userId": 1, "productId": 1}
            ],
            "products": [
                {"id": 1, "name": "Laptop", "stock": 0}
            ]
        }

        request = self.factory.post(
            '/recommendations/user/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = user_recommendations(request)

        data = json.loads(response.content)

        self.assertEqual(len(data['recommendations']), 0)

    # Test that no more than 5 recommendations are returned
    def test_returns_maximum_of_five_recommendations(self):
        body = {
            "userId": 1,
            "sales": [
                {"userId": 1, "productId": 1},
                {"userId": 1, "productId": 2},
                {"userId": 1, "productId": 3},
                {"userId": 1, "productId": 4},
                {"userId": 1, "productId": 5},
                {"userId": 1, "productId": 6}
            ],
            "products": [
                {"id": 1, "stock": 10},
                {"id": 2, "stock": 10},
                {"id": 3, "stock": 10},
                {"id": 4, "stock": 10},
                {"id": 5, "stock": 10},
                {"id": 6, "stock": 10}
            ]
        }

        request = self.factory.post(
            '/recommendations/user/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = user_recommendations(request)

        data = json.loads(response.content)

        self.assertLessEqual(len(data['recommendations']), 5)


# =========================================================
# Tests for max price recommendations endpoint
# =========================================================

class PriceMaxRecommendationsTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Test that only products under the maximum price are returned
    def test_returns_products_under_maximum_price(self):
        body = {
            "maxPrice": 100,
            "sales": [
                {"productId": 1, "quantity": 10},
                {"productId": 2, "quantity": 5}
            ],
            "products": [
                {"id": 1, "name": "Laptop", "stock": 10, "price": 90},
                {"id": 2, "name": "Phone", "stock": 10, "price": 150}
            ]
        }

        request = self.factory.post(
            '/recommendations/price-max/',
            data=json.dumps(body),
            content_type='application/json'
        )

        response = price_max_recommendations(request)

        data = json.loads(response.content)

        # Validate successful response
        self.assertEqual(response.status_code, 200)

        # Validate number of recommendations
        self.assertEqual(len(data['recommendations']), 1)

        # Validate returned product
        self.assertEqual(data['recommendations'][0]['id'], 1)

        # Validate product price condition
        self.assertTrue(data['recommendations'][0]['price'] <= 100)