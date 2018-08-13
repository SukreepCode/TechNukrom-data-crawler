import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


def init_env():
    # Use a service account
    service_key = {
        "type": "service_account",
        "project_id": "technukrom",
        "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
        "private_key": os.environ.get('PRIVATE_KEY'),
        "client_email": "data-crawler@technukrom.iam.gserviceaccount.com",
        "client_id": "110400317028019650866",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-crawler%40technukrom.iam.gserviceaccount.com"
    }
    print(service_key)
    cred = credentials.Certificate(service_key)
    firebase_admin.initialize_app(cred)
    return firestore.client()


def init():
    # Use a service account
    cred = credentials.Certificate('firebase-service-key.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()
