import unittest
import requests


class AppTest(unittest.TestCase):
    base_url = "http://ae9b2b34cb438470aa29151e53e1c565-836374029.ap-southeast-1.elb.amazonaws.com"

    def test_health_check(self):
        url = f"{self.base_url}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_endpoint(self):
        url = f"{self.base_url}/invalid-endpoint"
        response = requests.get(url)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
