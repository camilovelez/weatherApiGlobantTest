from datetime import datetime
import json
import os

script_dir = os.path.dirname(__file__)
filepath = './wind_config.json'
with open(os.path.join(script_dir, filepath)) as f:
    config_data = json.load(f)


class WeatherData:

    def __init__(self, data):

        time_zone_correction = data["timezone"]

        sunset_timestamp = self.convert_unix_timestamp(data["sys"]["sunset"] - time_zone_correction)
        self.sunset = self.get_hour_and_minute_from_timestamp(sunset_timestamp)
            
        sunrise_timestamp = self.convert_unix_timestamp(data["sys"]["sunrise"] - time_zone_correction)
        self.sunrise = self.get_hour_and_minute_from_timestamp(sunrise_timestamp)

        self.location_name = f"{data['name']},{data['sys']['country']}"
        self.geo_coordinates = [data["coord"]["lat"], data["coord"]["lon"]]
        self.requested_time = self.convert_unix_timestamp(data["dt"])
        self.cloudiness = data["weather"][0]["description"]
        self.wind_description = self.get_wind_description(data["wind"]["speed"], data["wind"]["deg"])
        self.temperature = f"{data['main']['temp']} °C"
        self.pressure = f"{data['main']['pressure']} hpa"
        self.humidity = f"{data['main']['humidity']} %"

    def convert_unix_timestamp(self, time_stamp):
        return datetime.utcfromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    
    def get_hour_and_minute_from_timestamp(self, timestamp):
        split_string = timestamp.split(" ")[1].split(":")
        return f"{split_string[0]}:{split_string[1]}"

    def get_wind_description(self, wind_speed, wind_direction):
        description = config_data["wind_descriptions"][-1]
        for index, ws in enumerate(config_data["wind_speeds"]):
            if wind_speed <= ws:
                description = config_data["wind_descriptions"][index]
                break
        
        direction = "north"
        for wd in config_data["wind_directions"]:
            if wind_direction >= wd["lower_limit"] and wind_direction < wd["upper_limit"]:
                direction = wd["direction"]

        return f"{description}, {wind_speed} m/s, {direction}"
    
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
                "humidity": self.humidity}

    def as_string(self):
        return json.dumps(self.as_dict())