from datetime import datetime
import json
import os

script_dir = os.path.dirname(__file__)
filepath = './wind_config.json'
with open(os.path.join(script_dir, filepath)) as f:
    config_data = json.load(f)


class WeatherData:

    def __init__(self, data):

        formats = dict()

        formats["wind_description"] = self.get_wind_description(data.get("wind").get("speed"), data.get("wind").get("deg", -1))

        time_zone_correction = data["timezone"]

        sunset_timestamp = self.convert_unix_timestamp(data.get("sys").get("sunset") - time_zone_correction)
        formats["sunset"] = self.get_hour_and_minute_from_timestamp(sunset_timestamp)
            
        sunrise_timestamp = self.convert_unix_timestamp(data.get("sys").get("sunrise") - time_zone_correction)
        formats["sunrise"] = self.get_hour_and_minute_from_timestamp(sunrise_timestamp)

        formats["requested_time"] = self.convert_unix_timestamp(data.get("dt"))

        self.proper_formats = all(value != "" for value in formats.values())

        if self.proper_formats:
            self.wind_description = formats.get("wind_description")
            
            self.sunset = formats.get("sunset")
            self.sunrise = formats.get("sunrise")
            self.requested_time = formats.get("requested_time")

            self.location_name = f"{data.get('name')},{data.get('sys').get('country')}"
            self.geo_coordinates = [data.get("coord").get("lat"), data.get("coord").get("lon")]
            
            self.cloudiness = data.get("weather")[0].get("description")
            
            self.temperature = f"{data.get('main').get('temp')} °C"
            self.pressure = f"{data.get('main').get('pressure')} hpa"
            self.humidity = f"{data.get('main').get('humidity')} %"

    def convert_unix_timestamp(self, time_stamp):
        try:
            return datetime.utcfromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ""
    
    def get_hour_and_minute_from_timestamp(self, timestamp):
        try:
            split_string = timestamp.split(" ")[1].split(":")
            return f"{split_string[0]}:{split_string[1]}"
        except:
            return ""

    def get_wind_description(self, wind_speed, wind_direction):
        if wind_direction > -1 and wind_direction <= 360:
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
        else:
            return ""
    
    def as_dict(self):
        if self.proper_formats:
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
        else:
            return {"error_message" : "data dont match expected formats"}