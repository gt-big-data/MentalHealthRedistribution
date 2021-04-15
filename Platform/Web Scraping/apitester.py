
import requests
import json

url = "http://127.0.0.1:5000/county_info"
county_list = ["Autauga County, Alabama", "Baldwin County, Alabama"]
parameters = {
#'county': "Autauga County, Alabama",
'counties': county_list
}
response = requests.get(url, params=parameters)
print(response.content)