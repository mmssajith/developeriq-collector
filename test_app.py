import unittest
from flask import json
from app import app, engine, metadata


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        metadata.create_all(engine)

    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {"status": "service is healthy"})

    def test_invalid_endpoint(self):
        response = self.app.get('/invalid-endpoint')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
