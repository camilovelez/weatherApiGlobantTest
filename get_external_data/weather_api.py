import requests

class WeatherApi:

    def __init__(self, url, api_id, weather_endpoint, forecast_endpoint):
        self.request_session = requests.Session()
        self.url = url
        self.api_id = api_id
        self.weather_endpoint = weather_endpoint
        self.forecast_endpoint = forecast_endpoint


    def make_request(self, city, country, endpoint):
        response_data = dict()
        status_code = 400
        try:
            query_params = f"?q={city},{country}&units=metric&appid={self.api_id}"
            requests_current_weather_api = self.request_session.get(self.url + endpoint + query_params)
            response_data = requests_current_weather_api.json()
            status_code = requests_current_weather_api.status_code
        except Exception as e:
            print(e)
        return response_data, status_code

    def get_weather_data(self, city, country):
        response_data, status_code =self.make_request(city,country, self.weather_endpoint)
        return response_data, status_code 

    def get_forecast_data(self, city, country):
        response_data, status_code = self.make_request(city,country, self.forecast_endpoint)
        return response_data, status_code 

    def get_data(self, city, country):
        weather_response_data, weather_status = self.get_weather_data(city, country)
        forecast_response_data, forecast_status = self.get_forecast_data(city, country)
        return weather_response_data, weather_status, forecast_response_data, forecast_status