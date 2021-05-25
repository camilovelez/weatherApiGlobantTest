import unittest
import requests

from get_external_data.weather_api import WeatherApi

from data_handling.weather_data import WeatherData
from data_handling.data_formatting import *

from app import API_URL, API_ID, WEATHER_ENDPOINT, FORECAST_ENDPOINT

class TestStringMethods(unittest.TestCase):

    def test_request_parameters(self):
        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Med111ellin&country=co")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=22")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=1&country=22")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin!!&country=co")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=cooo")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=c")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather")
        self.assertEqual(test_request.status_code, 400)
        self.assertEqual(test_request.json()["message"], "city and country must be provided and contain only letters, country must be 2 letters long")

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=co")
        self.assertEqual(test_request.status_code, 200)

        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=cO")
        self.assertEqual(test_request.status_code, 200)
        
        test_request = requests.get("http://127.0.0.1:5000/weather?city=Medellin&country=Co")
        self.assertEqual(test_request.status_code, 200)

    def test_get_weather_data(self):

        weather_api = WeatherApi(API_URL, API_ID, WEATHER_ENDPOINT, FORECAST_ENDPOINT)

        response_data, status_code = weather_api.get_weather_data("Medellin", "pe")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = weather_api.get_weather_data("Lima", "co")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = weather_api.get_weather_data("a", "pe")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = weather_api.get_weather_data("Medellin", "co")
        self.assertEqual(status_code, 200)
        
        weather_api.close_session()

    
    def test_get_forecast_data(self):

        weather_api = WeatherApi(API_URL, API_ID, WEATHER_ENDPOINT, FORECAST_ENDPOINT)

        response_data, status_code = weather_api.get_forecast_data("Medellin", "pe")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = weather_api.get_forecast_data("Lima", "co")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = weather_api.get_forecast_data("a", "pe")
        self.assertEqual(status_code, 404)
        self.assertEqual(response_data["message"], "city not found")

        response_data, status_code = weather_api.get_forecast_data("Medellin", "co")
        self.assertEqual(status_code, 200)

        weather_api.close_session()

    
    def test_get_data(self):

        weather_api = WeatherApi(API_URL, API_ID, WEATHER_ENDPOINT, FORECAST_ENDPOINT)

        (weather_response_data, weather_status, 
            forecast_response_data, forecast_status) = weather_api.get_data("Medellin", "pe")
        
        self.assertEqual(weather_status, 404)
        self.assertEqual(weather_response_data["message"], "city not found")
        self.assertEqual(forecast_status, 404)
        self.assertEqual(forecast_response_data["message"], "an error occured while requesting weather data")

        (weather_response_data, weather_status, 
            forecast_response_data, forecast_status) = weather_api.get_data("Lima", "co")
        
        self.assertEqual(weather_status, 404)
        self.assertEqual(weather_response_data["message"], "city not found")
        self.assertEqual(forecast_status, 404)
        self.assertEqual(forecast_response_data["message"], "an error occured while requesting weather data")

        (weather_response_data, weather_status, 
            forecast_response_data, forecast_status) = weather_api.get_data("a", "co")
        
        self.assertEqual(weather_status, 404)
        self.assertEqual(weather_response_data["message"], "city not found")
        self.assertEqual(forecast_status, 404)
        self.assertEqual(forecast_response_data["message"], "an error occured while requesting weather data")

        (weather_response_data, weather_status, 
            forecast_response_data, forecast_status) = weather_api.get_data("Medellin", "co")
        
        self.assertEqual(weather_status, 200)
        self.assertEqual(forecast_status, 200)

        weather_api.close_session()

        
    
    
    def test_convert_unix_timestamp(self):
        self.assertEqual(convert_unix_timestamp(1621810813), "2021-05-23 23:00:13")
        self.assertEqual(convert_unix_timestamp("2021-05-23 23:00:13"), "")
        self.assertEqual(convert_unix_timestamp("23:00:13"), "")
        self.assertEqual(convert_unix_timestamp("2021-05-23"), "")

    def test_get_hour_and_minute_from_timestamp(self):
        self.assertEqual(get_hour_and_minute_from_timestamp(1621810813), "23:00")
        self.assertEqual(get_hour_and_minute_from_timestamp("2021-05-23 23:00:13"), "")
        self.assertEqual(get_hour_and_minute_from_timestamp("23:00:13"), "")
        self.assertEqual(get_hour_and_minute_from_timestamp("2021-05-23"), "")

    def test_get_wind_description(self):
        self.assertEqual(get_wind_description(1.29, 71), "Gentle breeze, 1.29 m/s, east-northeast")
        self.assertEqual(get_wind_description(1.29, 371), "")
        self.assertEqual(get_wind_description(1.29, -1), "")
        self.assertEqual(get_wind_description(-1.29, -1), "")
        self.assertEqual(get_wind_description(-1.29, 71), "")
        self.assertEqual(get_wind_description("1.29 m/s", 1), "")
        self.assertEqual(get_wind_description("1.29 m/s", "1"), "")
        self.assertEqual(get_wind_description(1.29, "71"), "")

    def test_format_temperature(self):
        self.assertEqual(format_temperature(10), "10 °C")
        self.assertEqual(format_temperature(-10), "-10 °C")
        self.assertEqual(format_temperature(10.45), "10.45 °C")
        self.assertEqual(format_temperature(-10.45), "-10.45 °C")
        self.assertEqual(format_temperature(-273.1), "-273.1 °C")
        self.assertEqual(format_temperature(-273.2), "")
        self.assertEqual(format_temperature("15"), "")
        self.assertEqual(format_temperature("15 °C"), "")

    def test_format_pressure(self):
        self.assertEqual(format_pressure(10), "10 hpa")
        self.assertEqual(format_pressure(-0.4), "-0.4 hpa")
        self.assertEqual(format_pressure(10.45), "10.45 hpa")
        self.assertEqual(format_pressure(0.45), "0.45 hpa")
        self.assertEqual(format_pressure("15"), "")
        self.assertEqual(format_pressure("15 hpa"), "")

    def test_format_precipitation(self):
        self.assertEqual(format_precipitation(1), "100 %")
        self.assertEqual(format_precipitation(-0.4), "")
        self.assertEqual(format_precipitation(0.45), "45 %")
        self.assertEqual(format_precipitation(1.1), "")
        self.assertEqual(format_precipitation(0), "0 %")
        self.assertEqual(format_precipitation("1"), "")

    def test_format_humidity(self):
        self.assertEqual(format_humidity(1), "1 %")
        self.assertEqual(format_humidity(100), "100 %")
        self.assertEqual(format_humidity(-0.4), "")
        self.assertEqual(format_humidity(45), "45 %")
        self.assertEqual(format_humidity(10.1), "10.1 %")
        self.assertEqual(format_humidity(0), "0 %")
        self.assertEqual(format_humidity("1"), "")
    
    
    
    def test_validate_formats(self):

        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 
            'visibility': 8410, 'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 
            'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        forecast_data = ({"cod":"200","message":0,"cnt":40,"list":[{"dt":1621868400,"main":{"temp":16.73,"feels_like":16.76,"temp_min":12.43,"temp_max":16.73,"pressure":1020,"sea_level":1020,"grnd_level":755,"humidity":88,"temp_kf":4.3},
            "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":75},"wind":{"speed":1.35,"deg":132,"gust":2.62},"visibility":10000,"pop":0.56,"rain":{"3h":0.32},"sys":{"pod":"d"},"dt_txt":"2021-05-24 15:00:00"}
            ,{"dt":1621879200,"main":{"temp":16.08,"feels_like":15.96,"temp_min":14.78,"temp_max":16.08,"pressure":1019,"sea_level":1019,"grnd_level":754,"humidity":85,"temp_kf":1.3},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],
            "clouds":{"all":80},"wind":{"speed":1.84,"deg":140,"gust":3.03},"visibility":10000,"pop":0.66,"rain":{"3h":0.27},"sys":{"pod":"d"},"dt_txt":"2021-05-24 18:00:00"}],"city":{"id":3688689,"name":"Bogotá","coord":{"lat":4.6097,"lon":-74.0817},"country":"CO",
            "population":1000000,"timezone":-18000,"sunrise":1621852965,"sunset":1621897438}})

        self.assertEqual(validate_formats(weather_data, forecast_data), True)

        #changed the format of the requested time, "dt" in weather data
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
            'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
            'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': "10:24", 
            'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #added a wind direction degree bellow 360, "deg" in weather data
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
            'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
            'wind': {'speed': 1.29, 'deg': 571, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 
            'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #no wind direction, "deg" in weather data
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 
            'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 'visibility': 8410, 
            'wind': {'speed': 1.29, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 
            'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #temperature bellow -273.15 C
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': -319.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 
            'visibility': 8410, 'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 
            'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #temperature bellow -273.15 C
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': -319.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 
            'visibility': 8410, 'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 
            'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #over 100% of humidity
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 'pressure': 1012, 'humidity': 103, 'sea_level': 1012, 'grnd_level': 850}, 
            'visibility': 8410, 'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 
            'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #just resetting weather data to a correct value
        weather_data = ({'coord': {'lon': -75.5636, 'lat': 6.2518}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
            'base': 'stations', 'main': {'temp': 19.26, 'feels_like': 19.67, 'temp_min': 19.26, 'temp_max': 19.26, 'pressure': 1012, 'humidity': 93, 'sea_level': 1012, 'grnd_level': 850}, 
            'visibility': 8410, 'wind': {'speed': 1.29, 'deg': 71, 'gust': 1.7}, 'clouds': {'all': 74}, 'dt': 1621810813, 'sys': {'country': 'CO', 'sunrise': 1621766769, 'sunset': 1621811534}, 
            'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200})

        #no forecast data
        forecast_data = ({"cod":"200","message":0,"cnt":40,"list":[],"city":{"id":3688689,"name":"Bogotá","coord":{"lat":4.6097,"lon":-74.0817},"country":"CO",
            "population":1000000,"timezone":-18000,"sunrise":1621852965,"sunset":1621897438}})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #temperature bellow -273.15 C
        forecast_data = ({"cod":"200","message":0,"cnt":40,"list":[{"dt":1621868400,"main":{"temp":-316.73,"feels_like":16.76,"temp_min":12.43,"temp_max":16.73,"pressure":1020,"sea_level":1020,"grnd_level":755,"humidity":88,"temp_kf":4.3},
            "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":75},"wind":{"speed":1.35,"deg":132,"gust":2.62},"visibility":10000,"pop":0.56,"rain":{"3h":0.32},"sys":{"pod":"d"},"dt_txt":"2021-05-24 15:00:00"}
            ,{"dt":1621879200,"main":{"temp":16.08,"feels_like":15.96,"temp_min":14.78,"temp_max":16.08,"pressure":1019,"sea_level":1019,"grnd_level":754,"humidity":85,"temp_kf":1.3},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],
            "clouds":{"all":80},"wind":{"speed":1.84,"deg":140,"gust":3.03},"visibility":10000,"pop":0.66,"rain":{"3h":0.27},"sys":{"pod":"d"},"dt_txt":"2021-05-24 18:00:00"}],"city":{"id":3688689,"name":"Bogotá","coord":{"lat":4.6097,"lon":-74.0817},"country":"CO",
            "population":1000000,"timezone":-18000,"sunrise":1621852965,"sunset":1621897438}})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #negative humidity
        forecast_data = ({"cod":"200","message":0,"cnt":40,"list":[{"dt":1621868400,"main":{"temp":16.73,"feels_like":16.76,"temp_min":12.43,"temp_max":16.73,"pressure":1020,"sea_level":1020,"grnd_level":755,"humidity":-88,"temp_kf":4.3},
            "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":75},"wind":{"speed":1.35,"deg":132,"gust":2.62},"visibility":10000,"pop":0.56,"rain":{"3h":0.32},"sys":{"pod":"d"},"dt_txt":"2021-05-24 15:00:00"}
            ,{"dt":1621879200,"main":{"temp":16.08,"feels_like":15.96,"temp_min":14.78,"temp_max":16.08,"pressure":1019,"sea_level":1019,"grnd_level":754,"humidity":85,"temp_kf":1.3},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],
            "clouds":{"all":80},"wind":{"speed":1.84,"deg":140,"gust":3.03},"visibility":10000,"pop":0.66,"rain":{"3h":0.27},"sys":{"pod":"d"},"dt_txt":"2021-05-24 18:00:00"}],"city":{"id":3688689,"name":"Bogotá","coord":{"lat":4.6097,"lon":-74.0817},"country":"CO",
            "population":1000000,"timezone":-18000,"sunrise":1621852965,"sunset":1621897438}})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)

        #negative precipitation
        forecast_data = ({"cod":"200","message":0,"cnt":40,"list":[{"dt":1621868400,"main":{"temp":16.73,"feels_like":16.76,"temp_min":12.43,"temp_max":16.73,"pressure":1020,"sea_level":1020,"grnd_level":755,"humidity":88,"temp_kf":4.3},
            "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":75},"wind":{"speed":1.35,"deg":132,"gust":2.62},"visibility":10000,"pop":-0.56,"rain":{"3h":0.32},"sys":{"pod":"d"},"dt_txt":"2021-05-24 15:00:00"}
            ,{"dt":1621879200,"main":{"temp":16.08,"feels_like":15.96,"temp_min":14.78,"temp_max":16.08,"pressure":1019,"sea_level":1019,"grnd_level":754,"humidity":85,"temp_kf":1.3},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],
            "clouds":{"all":80},"wind":{"speed":1.84,"deg":140,"gust":3.03},"visibility":10000,"pop":0.66,"rain":{"3h":0.27},"sys":{"pod":"d"},"dt_txt":"2021-05-24 18:00:00"}],"city":{"id":3688689,"name":"Bogotá","coord":{"lat":4.6097,"lon":-74.0817},"country":"CO",
            "population":1000000,"timezone":-18000,"sunrise":1621852965,"sunset":1621897438}})

        self.assertEqual(validate_formats(weather_data, forecast_data), False)




if __name__ == '__main__':
    unittest.main()