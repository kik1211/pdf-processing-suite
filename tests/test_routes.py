import os
import sys
import unittest

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_all_get_routes(self):
        routes = [
            '/',
            '/invert',
            '/merge',
            '/split',
            '/compress',
            '/watermark',
            '/rotate',
            '/add_blank',
            '/paste_image',
            '/edit_pages',
            '/batch_invert',
        ]
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Route {route} failed with status code {response.status_code}"
                )

    def test_invalid_endpoint_returns_404(self):
        response = self.client.get('/nonexistent_route_404')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
