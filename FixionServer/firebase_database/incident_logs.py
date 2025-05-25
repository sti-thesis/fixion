from firebase_admin import firestore

db = firestore.client()

# Create a new Incident Log
def create_incident_log(machine_ID, user_id, log_type, message):
    db.collection("IncidentLogs_Tb").document(machine_ID).set({
        "machine_ID": machine_ID,
        "user_id": user_id,
        "log_type": log_type,
        "message": message,
        "created_at": firestore.SERVER_TIMESTAMP
    })

# Read an Incident Log by Machine ID
def get_incident_log(machine_ID):
    doc = db.collection("IncidentLogs_Tb").document(machine_ID).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update an Incident Log by Machine ID
def update_incident_log(machine_ID, data):
    db.collection("IncidentLogs_Tb").document(machine_ID).update(data)

# Delete an Incident Log by Machine ID
def delete_incident_log(machine_ID):
    db.collection("IncidentLogs_Tb").document(machine_ID).delete()
