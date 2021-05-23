from flask import Flask, Response, request
import requests
import os
from flask_caching import Cache
import json

from data_handling.weather_data import WeatherData

DEBUG = True

if DEBUG:
    os.environ["API_ID"] = "1508a9a4840a5574c822d70ca2132032"
    os.environ["WEATHER_URL"] = "http://api.openweathermap.org/data/2.5/"
    os.environ["WEATHER_ENDPOINT"] = "weather"
    os.environ["CACHE_TYPE"] = "SimpleCache"
    os.environ["CACHE_DEFAULT_TIMEOUT"] = "120"

API_ID = os.environ.get("API_ID")
WEATHER_URL =  os.environ.get("WEATHER_URL")
WEATHER_ENDPOINT = os.environ.get("WEATHER_ENDPOINT")
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


def request_weather_api(city, country):
    response_data = dict()
    status_code = 400
    try:
        query_params = f"?q={city},{country}&units=metric&appid={API_ID}"
        requests_weather_api = requests.get(WEATHER_URL + WEATHER_ENDPOINT + query_params)
        if requests_weather_api.status_code == 200:
            response_data = requests_weather_api.json()
            status_code = requests_weather_api.status_code
    except Exception as e:
        print(e)
    return response_data, status_code

@app.route("/weather")   
def weather():
    response_data = dict()
    status_code = 400

    # response_weather_api, status_code = json.loads('{"coord":{"lon":-74.0817,"lat":4.6097},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"base":"stations","main":{"temp":18.73,"feels_like":18.43,"temp_min":18.73,"temp_max":18.73,"pressure":1014,"humidity":68,"sea_level":1014,"grnd_level":755},"visibility":10000,"wind":{"speed":1.69,"deg":163,"gust":2.98},"clouds":{"all":75},"dt":1621704337,"sys":{"type":1,"id":8582,"country":"CO","sunrise":1621680163,"sunset":1621724618},"timezone":-18000,"id":3688689,"name":"Bogotá","cod":200}'), 200

    city = request.args.get("city")
    country = request.args.get("country")

    if type(city) == str and type(country)==str:
        cache_key = f"{city},{country}"
        cached_data = cache.get(cache_key)
        if cached_data is None:
            response_weather_api, status_code = request_weather_api(city, country.lower())
            if status_code == 200: 
                response_data = WeatherData(response_weather_api).as_string()
                if cache_key in cache.cache._cache:
                    cache.delete(cache_key)
                cache.add(cache_key, response_data)
        else:
            response_data = cached_data
            status_code = 200
    
    return Response(response_data,
                    status=status_code,
                    mimetype='application/json')

