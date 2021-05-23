import unittest
import requests
from app import request_weather_api

class TestStringMethods(unittest.TestCase):

    def test_request_parameters(self):
        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Med111ellin&country=co")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=22")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=1&country=22")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin!!&country=co")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=cooo")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=c")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["error_message"], "city and country must be provided and contain only letters, country must be 2 letters long")

    def test_external_api_call(self):
        response_data, status_code = request_weather_api("Medellin", "pe")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = request_weather_api("Lima", "co")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = request_weather_api("a", "pe")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = request_weather_api("Medellin", "co")
        self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()