from datetime import datetime
import os
import json

script_dir = os.path.dirname(__file__)
filepath = './wind_config.json'
with open(os.path.join(script_dir, filepath)) as f:
    config_data = json.load(f)

def convert_unix_timestamp(time_stamp):
    try:
        return datetime.utcfromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Exception thrown while validating converting timestamp: {e}")
        return ""
    
def get_hour_and_minute_from_timestamp(unix_timestamp):
    try:
        timestamp = convert_unix_timestamp(unix_timestamp).split(" ")[1].split(":")
        return f"{timestamp[0]}:{timestamp[1]}"
    except Exception as e:
        print(f"Exception thrown while gettting hour and minute from timestamp: {e}")
        return ""

def get_wind_description(wind_speed, wind_direction):
    try:
        if wind_speed >= 0 and wind_direction >= 0 and wind_direction <= 360:
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
    except Exception as e:
        print(f"Exception thrown while getting wind description: {e}")
        return ""

def format_temperature(temperature):
    if temperature is not None and (type(temperature) == float or type(temperature) == int) and temperature >= -273.15:
        return f"{temperature} °C"
    else:
        return ""

def format_pressure(pressure):
    if pressure is not None and (type(pressure) == int or type(pressure) == float):
        return f"{pressure} hpa"
    else:
        return ""

def format_humidity(humidity):
    if humidity is not None and (type(humidity) == int or type(humidity) == float) and humidity >= 0 and humidity <= 100:
        return f"{humidity} %"
    else:
        return ""
    

def format_precipitation(precipitation):
    if (precipitation is not None and (type(precipitation) == float or type(precipitation) == int) 
        and precipitation >= 0 and precipitation <= 1):

        return f"{int(precipitation * 100)} %"
    else:
        return ""

def validate_formats(weather_data, forecast_data):
    formats = dict()

    formats["wind_description"] = get_wind_description(weather_data.get("wind").get("speed"), weather_data.get("wind").get("deg", -1))

    time_zone_correction = weather_data["timezone"]

    formats["sunset"] = get_hour_and_minute_from_timestamp(weather_data.get("sys").get("sunset") - time_zone_correction)
        
    formats["sunrise"] = get_hour_and_minute_from_timestamp(weather_data.get("sys").get("sunrise") - time_zone_correction)

    formats["requested_time"] = convert_unix_timestamp(weather_data.get("dt"))

    formats["temperature"] = format_temperature(weather_data.get('main').get('temp'))

    formats["pressure"] = format_pressure(weather_data.get('main').get('pressure'))

    formats["humidity"] = format_humidity(weather_data.get('main').get('humidity'))


    try:
    
        first_forecast = forecast_data.get("list")[0]

        formats["forecast_temperature"] = format_temperature(first_forecast.get('main').get('temp'))

        formats["forecast_pressure"] = format_pressure(first_forecast.get('main').get('pressure'))

        formats["forecast_humidity"] = format_humidity(first_forecast.get('main').get('humidity'))

        formats["forecast_precipitation"] = format_precipitation(first_forecast.get("pop"))

        return all(value != "" for value in formats.values())
    except Exception as e:
        print(f"Exception thrown while validating all formats: {e}")
        return False