import unittest
from app.main import app

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_discover_endpoint(self):
        response = self.client.post('/api/v1/discover')
        self.assertEqual(response.status_code, 200)
        self.assertIn('devices', response.json)

    def test_invalid_request(self):
        response = self.client.post('/api/v1/discover', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()