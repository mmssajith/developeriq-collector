import unittest
import requests


class AppTest(unittest.TestCase):
    base_url = "http://acedad2df4da14730b8937257b26fd69-1780538901.ap-southeast-1.elb.amazonaws.com"

    def test_health_check(self):
        url = f"{self.base_url}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"status": "service is healthy"})

    def test_invalid_endpoint(self):
        url = f"{self.base_url}/invalid-endpoint"
        response = requests.get(url)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
