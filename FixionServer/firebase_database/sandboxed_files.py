# sandboxed_files.py
from firebase_admin import firestore

db = firestore.client()

# Create a new Sandboxed File
def create_sandboxed_file(threat_id, file_name, file_hash, status):
    db.collection("SandboxedFiles_Tb").document(file_hash).set({
        "threat_id": threat_id,
        "file_name": file_name,
        "file_hash": file_hash,
        "status": status,
        "sandboxed_at": firestore.SERVER_TIMESTAMP
    })

# Read a Sandboxed File by File Hash
def get_sandboxed_file(file_hash):
    doc = db.collection("SandboxedFiles_Tb").document(file_hash).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Sandboxed File by File Hash
def update_sandboxed_file(file_hash, data):
    db.collection("SandboxedFiles_Tb").document(file_hash).update(data)

# Delete a Sandboxed File by File Hash
def delete_sandboxed_file(file_hash):
    db.collection("SandboxedFiles_Tb").document(file_hash).delete()
