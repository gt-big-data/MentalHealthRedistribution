from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import os.path as path
import json

firebase_credentials_path = os.getcwd()
firebase_credentials_path += "/mental-health-redistribution-firebase-adminsdk-j3xlw-617de04f19.json"
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)
cred = credentials.ApplicationDefault()
db = firestore.client()

def scraper():
	print("Scrape Web here")

scheduler = BackgroundScheduler(daemon=True)

scheduler.add_job(scraper,'interval',minutes=1440)

scheduler.start()

#http://127.0.0.1:5000/potential_mental_health_centers


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

if __name__ == "__main__":
	app.run()




