import requests
import json
import csv
# from geopy.geocoders import Nominatim

def geocache(address):
    API_KEY = "pk.48ea123c6f85b80a2906323f9accf101"
    components = address.split(",")
    url = "https://us1.locationiq.com/v1/search.php"
    data = {
        'key': API_KEY,
        'street': components[0],
        # 'city': components[1],
        # 'state': components[2],
        'country': 'US',
        'format': 'json'
    }
    response = requests.get(url, params=data)
    json_file = json.loads(response.content)
    lat = json_file[0]["lat"]
    lon = json_file[0]["lon"]
    return lat, lon


jsonList = []

for i in range(1, 4):
    print(str(i))
    with open("current_mental_health_centers_" + str(i) + ".csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data = {}
            data["name"] = row[1]
            data["description"] = row[2]
            try:
                location = geocache(row[4])
                data["latitude"] = location[0]
                data["longitude"] = location[1]
            except:
                data["latitude"] = "None"
                data["longitude"] = "None"  
            jsonList.append(data)      

with open("data.json", "w") as f:
    json.dump(jsonList, f, indent=4)

# location = locator.geocode("88217 Highway 9 ")
# print(location.latitude)
# print(location.longitude)