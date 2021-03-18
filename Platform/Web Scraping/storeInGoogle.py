import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import os.path as path


firebase_credentials_path =  path.abspath(path.join(__file__ ,"../../.."))
firebase_credentials_path += "/mental-health-redistribution-firebase-adminsdk-j3xlw-a8e9757a35.json"

cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)


cred = credentials.ApplicationDefault()

'''
firebase_admin.initialize_app(cred, {
  'projectId': "mental-health-redistribution",
})
'''

db = firestore.client()



def storeInGoogle(address):
	doc_ref = db.collection(u'addresses').document(address)
	doc_ref.set({
		u'address': address,
		u'lat': 0,
		u'long': 0
	})

storeInGoogle("333 Central Expy N, Allen, TX")