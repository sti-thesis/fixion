# threats.py
from firebase_admin import firestore

db = firestore.client()

# Create a new Threat
def create_threat(threat_id, threatlevel_id, machine_id, file_path, threat_type, detected_by):
    db.collection("Threats_Tb").document(threat_id).set({
        "threatlevel_id": threatlevel_id,
        "machine_id": machine_id,
        "file_path": file_path,
        "threat_type": threat_type,
        "detected_by": detected_by,
        "time_detected": firestore.SERVER_TIMESTAMP,
        "status": "pending"
    })

# Read a Threat by ID
def get_threat(threat_id):
    doc = db.collection("Threats_Tb").document(threat_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Threat by ID
def update_threat(threat_id, data):
    db.collection("Threats_Tb").document(threat_id).update(data)

# Delete a Threat by ID
def delete_threat(threat_id):
    db.collection("Threats_Tb").document(threat_id).delete()
