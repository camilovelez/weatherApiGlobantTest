import json

from .data_formatting import *
from .forecast import Forecast
from .weather import Weather

class WeatherData(Weather):

    def __init__(self, weather_data, forecast_data):

        super().__init__(weather_data)
        
        time_zone_correction = weather_data["timezone"]
        
        self.sunset = get_hour_and_minute_from_timestamp(weather_data.get("sys").get("sunset") - time_zone_correction)
        self.sunrise = get_hour_and_minute_from_timestamp(weather_data.get("sys").get("sunrise") - time_zone_correction)
        self.requested_time = convert_unix_timestamp(weather_data.get("dt"))

        self.location_name = f"{weather_data.get('name')},{weather_data.get('sys').get('country')}"
        self.geo_coordinates = [weather_data.get("coord").get("lat"), weather_data.get("coord").get("lon")]

        forecast_list = forecast_data.get("list")
        self.forecast = [Forecast(data).as_dict() for data in forecast_list]


    
    def as_dict(self):
        return {"sunset": self.sunset, 
                "sunrise": self.sunrise, 
                "location_name": self.location_name,
                "geo_coordinates": self.geo_coordinates,
                "requested_time": self.requested_time,
                "cloudiness": self.cloudiness,
                "wind_description": self.wind_description,
                "temperature": self.temperature,
                "pressure": self.pressure,
                "humidity": self.humidity,
                "forecast": self.forecast}
