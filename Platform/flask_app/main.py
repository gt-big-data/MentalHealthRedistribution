from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import os.path as path
import json
import csv
from scraper import scrape
from geocoder import get_lat_long
from optimalCenter import optimal_center_formula


firebase_credentials_path = os.getcwd()
firebase_credentials_path += "/mental-health-redistribution-firebase-adminsdk-j3xlw-617de04f19.json"

cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)
cred = credentials.ApplicationDefault()
db = firestore.client()

county_dictionary = {}
with open('county.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
    	county_dictionary[row["Location"]] = row

county_coords = {}
with open('county_coords.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
    	identifier = row["COUNAME"] + " County, " + row["STNAME"]
    	county_coords[identifier] = {}
    	county_coords[identifier]["lat"] = row["LATITUDE"]
    	county_coords[identifier]["lon"] = row["LONGITUDE"]

def store_scraped_in_google(address, name, lat, lon):
	doc_ref = db.collection(u'potentialLocations').document(name)
	doc_ref.set({
		u'Address': address,
		u'lat': lat,
		u'lon': lon
	})

def scraper():
	loopnetListings = scrape()
	j = 0
	name_set = {}
	for index, row in loopnetListings.iterrows():
		address_map = {}
		address = row[0]
		address_map['address'] = address
		components = address.split(",")
		try:
			address_map['street'] = components[0]
			address_map['city'] = components[1]
			address_map['state'] = components[2]
		except:
			print("Exception: invalid format of address")
			continue
		name = row[1]
		if name_set.get(name) == None:
			name_set[name] = 1
		else:
			name = name + " " + str(name_set.get(name))
		lat, lon = get_lat_long(address)
		try:
			store_scraped_in_google(address_map, name, lat, lon)
		except:
			print("Exception: Could not store in Google")


scheduler = BackgroundScheduler(daemon=True)

scheduler.add_job(scraper,'interval',minutes=1440)

scheduler.start()



app = Flask(__name__)

@app.route("/potential_mental_health_centers")
def potential_mental_health_centers():
	collection = db.collection(u'potentialLocations').where(u'lat', u'!=', 0).stream()
	response = []
	for doc in collection:
		response.append(doc.to_dict())
	return json.dumps(response)

@app.route("/current_mental_health_centers")
def current_mental_health_centers():
	collection = db.collection(u'currentLocations').where(u'lat', u'!=', 0).stream()
	response = []
	for doc in collection:
		response.append(doc.to_dict())
	return json.dumps(response)

@app.route("/county_info")
def county_info():
	return json.dumps(county_dictionary[request.args.get('county')])

@app.route("/optimal_centers")
def optimal_centers():
	county_list = request.args.getlist('counties')
	response = {}
	potential_locations = db.collection(u'potentialLocations').where(u'lat', u'!=', 0).stream()
	for doc in potential_locations:
		potential_lat = float(doc.to_dict()["lat"])
		potential_lon = float(doc.to_dict()["lon"])
		score = 0
		for county in county_list:
			county_lat = float(county_coords[county]["lat"])
			county_lon = float(county_coords[county]["lon"])
			county_classification = float(county_dictionary[county]["Mental Health Need Classification"])
			score += optimal_center_formula(county_lat, county_lon, potential_lat, potential_lon, county_classification)
		score = score/len(county_list)
		response[str(doc.id)] = {}
		response[str(doc.id)]["details"] = doc.to_dict()
		response[str(doc.id)]["score"] = score
	response = {key: value for key, value in sorted(response.items(), key = lambda item: item[1]['score'], reverse=True)}
	return json.dumps(response)

if __name__ == "__main__":
	app.run()