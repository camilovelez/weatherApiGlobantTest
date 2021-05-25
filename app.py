from flask import Flask, Response, request
import os
from flask_caching import Cache
import json

from data_handling.weather_data import WeatherData
from data_handling.data_formatting import validate_formats
from get_external_data.weather_api import WeatherApi

DEBUG = True

if DEBUG:
    os.environ["API_ID"] = "1508a9a4840a5574c822d70ca2132032"
    os.environ["API_URL"] = "http://api.openweathermap.org/data/2.5/"
    os.environ["WEATHER_ENDPOINT"] = "weather"
    os.environ["FORECAST_ENDPOINT"] = "forecast"
    os.environ["CACHE_TYPE"] = "SimpleCache"
    os.environ["CACHE_DEFAULT_TIMEOUT"] = "120"

API_ID = os.environ.get("API_ID")
API_URL =  os.environ.get("API_URL")
WEATHER_ENDPOINT = os.environ.get("WEATHER_ENDPOINT")
FORECAST_ENDPOINT = os.environ.get("FORECAST_ENDPOINT")
CACHE_TYPE = os.environ.get("CACHE_TYPE")
CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT"))

config = {
    "DEBUG": DEBUG,         
    "CACHE_TYPE": CACHE_TYPE,  
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT
}


app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)

@app.route("/weather")   
def weather():
    response_data = dict()
    status_code = 400

    city = request.args.get("city")
    country = request.args.get("country")

    if city is not None and city.isalpha() and country is not None and country.isalpha() and len(country) == 2:
        
        country = country.lower()
        cache_key = f"{city},{country}"
        cached_data = cache.get(cache_key)
        if cached_data is None:
            weather_api = WeatherApi(API_URL, API_ID, WEATHER_ENDPOINT, FORECAST_ENDPOINT)

            (response_data_weather, status_code_weather, 
            response_data_forecast, status_code_forecast) = weather_api.get_data(city, country)

            weather_api.close_session()

            if status_code_weather == 200 and status_code_forecast == 200:

                if validate_formats(response_data_weather, response_data_forecast):

                    status_code = 200
                    response_data = WeatherData(response_data_weather, response_data_forecast).as_dict()
                    if cache_key in cache.cache._cache:
                        cache.delete(cache_key)
                    cache.add(cache_key, response_data)
                else:
                    status_code = 404
                    response_data["message"] = "data dont match expected formats"

            elif status_code_weather != 200:
                status_code = status_code_weather
                response_data = response_data_weather
            
            elif status_code_forecast != 200:
                status_code = status_code_forecast
                response_data = response_data_forecast
            

        else:
            response_data = cached_data
            status_code = 200
    else:
        response_data["message"] = "city and country must be provided and contain only letters, country must be 2 letters long"
    
    return Response(json.dumps(response_data),
                    status=status_code,
                    mimetype="application/json")


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))