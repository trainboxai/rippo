from google.cloud import firestore, storage
import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate('rippo-777-firebase-adminsdk.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()

storage_client = storage.Client.from_service_account_json('rippo-777-firebase-adminsdk.json')
bucket = storage_client.get_bucket("rippo-777.appspot.com")