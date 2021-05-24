import json

from .data_formatting import *
from .weather import Weather


class Forecast(Weather):
    def __init__(self, forecast_data):

        super().__init__(forecast_data)
        
        self.forecast_time = forecast_data.get("dt_txt")

        # self.rain = format_rain(forecast_data.get("rain").get("3h"), -1)
        self.precipitation = format_precipitation(forecast_data.get("pop"))


    def as_dict(self):
        return {"forecast_time": self.forecast_time, 
                "cloudiness": self.cloudiness,
                "wind_description": self.wind_description,
                "temperature": self.temperature,
                "pressure": self.pressure,
                "humidity": self.humidity,
                # "rain": self.rain,
                "precipitation": self.precipitation}