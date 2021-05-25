from .data_formatting import *
from .shared_weather_data import SharedWeatherData


class Forecast(SharedWeatherData):
    def __init__(self, forecast_data):

        super().__init__(forecast_data)
        
        self.forecast_time = forecast_data.get("dt_txt")

        self.precipitation = format_precipitation(forecast_data.get("pop"))


    def as_dict(self):
        return {"forecast_time": self.forecast_time, 
                "cloudiness": self.cloudiness,
                "wind_description": self.wind_description,
                "temperature": self.temperature,
                "pressure": self.pressure,
                "humidity": self.humidity,
                "precipitation": self.precipitation}