import geopy
from geopy.extra.rate_limiter import RateLimiter
from geopy import ArcGIS
import json
import pandas as pd
import time


locator = ArcGIS(user_agent="myGeocode")

def get_lat_long(address):
    location = locator.geocode(address)
    if (location == None):
        time.sleep(3)
        API_KEY = "INSERT API KEY HERE"
        components = address.split(",")
        url = "https://us1.locationiq.com/v1/search.php"
        data = {
            'key': API_KEY,
            'street': components[0],
            'city': components[1],
            'state': components[2],
            'country': 'US',
            'format': 'json'
            }
        response = requests.get(url, params=data)
        json_file = json.loads(response.content)
        try:
            lat = json_file[0]["lat"]
            lon = json_file[0]["lon"]
            return lat, lon
        except:
            print(json_file)
            return 0,0
    return location.latitude, location.longitude






































#pk.c8010a15cec9339e30b016814eb61a6a