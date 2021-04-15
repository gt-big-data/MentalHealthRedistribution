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
#county.csv


firebase_credentials_path =  path.abspath(path.join(__file__ ,"../../.."))
firebase_credentials_path += "/mental-health-redistribution-firebase-adminsdk-j3xlw-a8e9757a35.json"

cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)
cred = credentials.ApplicationDefault()
db = firestore.client()

county_dictionary = {}
with open('county.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
    	county_dictionary[row["Location"]] = row

def store_scraped_in_google(address, name, lat, lon):
	doc_ref = db.collection(u'potentialLocations').document(name)
	doc_ref.set({
		u'Address': address,
		u'lat': lat,
		u'lon': lon
	})

def scraper():
	#delete_all_potential_locations()
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
#scheduler.add_job(scraper,'interval',minutes=5)

scheduler.start()

#http://127.0.0.1:5000/get_optimal_centers_list


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
	for county in county_list:
		potential_locations = db.collection(u'potentialLocations').where(u'lat', u'!=', 0).stream()
		county_lat = 43 #placeholder
		county_lon = -75.234213443 #placeholder
		county_classification = float(county_dictionary[county]["Mental Health Need Classification"])
		optimal_center = None
		max_optimality = 0
		name = ""
		for doc in potential_locations:
			potential_lat = float(doc.to_dict()["lat"])
			potential_lon = float(doc.to_dict()["lon"])
			optimality = optimal_center_formula(county_lat, county_lon, potential_lat, potential_lon, county_classification)
			if (optimality > max_optimality):
				optimal_center = doc.to_dict()
				max_optimality = optimality
				name = doc.id
		response[county] = optimal_center
		response[county]["name"] = name
	return json.dumps(response)

if __name__ == "__main__":
	app.run()




