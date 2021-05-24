import unittest
import requests
from app import request_weather_api, weather
from data_handling.weather_data import WeatherData

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
    
    def test_formats(self):
        weather_data = WeatherData({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
                                    'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
                                    'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
                                    'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 
                                    'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(weather_data.proper_formats, True)

        weather_data = WeatherData({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
                                    'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
                                    'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
                                    'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': "10:24", 
                                    'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(weather_data.proper_formats, False)
        self.assertEqual(weather_data.as_dict()["error_message"], "data dont match expected formats")

        weather_data = WeatherData({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
                                    'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
                                    'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
                                    'wind': {'speed': 1.29, 'deg': 571, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 
                                    'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(weather_data.proper_formats, False)
        self.assertEqual(weather_data.as_dict()["error_message"], "data dont match expected formats")

        weather_data = WeatherData({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
                                    'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
                                    'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
                                    'wind': {'speed': 1.29, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 
                                    'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(weather_data.proper_formats, False)
        self.assertEqual(weather_data.as_dict()["error_message"], "data dont match expected formats")

        fomarted_timestamp = weather_data.get_hour_and_minute_from_timestamp("2010-05-15 10_05_15")
        self.assertEqual(fomarted_timestamp, "")

if __name__ == '__main__':
    unittest.main()