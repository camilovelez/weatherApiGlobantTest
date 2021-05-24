from .data_formatting import *

class SharedWeatherData:
    
    def __init__(self, data):

        self.pressure = format_pressure(data.get("main").get("pressure"))
        self.temperature = format_temperature(data.get("main").get("temp"))
        self.humidity = format_humidity(data.get("main").get("humidity"))
        
        self.wind_description = get_wind_description(data.get("wind").get("speed"),
                                                     data.get("wind").get("deg", -1))

        self.cloudiness = data.get("weather")[0].get("description")