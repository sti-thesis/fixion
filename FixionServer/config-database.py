import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred = credentials.Certificate("fixion-database-security-key.json")
firebase_admin.initialize_app(cred)



