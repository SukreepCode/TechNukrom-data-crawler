import firebase_admin
from firebase_admin import credentials
# import firestore
from firebase_admin import firestore as db_firestore
# import firebase
from firebase_admin import db as db_firebase
import os

def get_cerd(env=True):
    if env == True:
        service_key = {
            "type": "service_account",
            "project_id": "technukrom",
            "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
            "private_key": os.environ.get('PRIVATE_KEY').replace('\\n','\n'),
            "client_email": "data-crawler@technukrom.iam.gserviceaccount.com",
            "client_id": "110400317028019650866",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-crawler%40technukrom.iam.gserviceaccount.com"
        }
        cred = credentials.Certificate(service_key)
    else:
        cred = credentials.Certificate('firebase-service-key.json')
    return cred

def init_firebase(env=True):
    firebase_admin.initialize_app(get_cerd(env),
        options={ 'databaseURL': 'https://technukrom.firebaseio.com'
        })
    return {
        'firebase': db_firebase,
        'firestore': db_firestore.client()
    }
