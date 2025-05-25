from firebase_admin import firestore

db = firestore.client()

# Create a new Threat Level
def create_threat_level(level_name, description, auto_response, requires_admin_approval):
    db.collection("ThreatLevels_Tb").document(level_name).set({
        "level_name": level_name,
        "description": description,
        "auto_response": auto_response,
        "requires_admin_approval": requires_admin_approval
    })

# Read a Threat Level by Name
def get_threat_level(level_name):
    doc = db.collection("ThreatLevels_Tb").document(level_name).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Threat Level by Name
def update_threat_level(level_name, data):
    db.collection("ThreatLevels_Tb").document(level_name).update(data)

# Delete a Threat Level by Name
def delete_threat_level(level_name):
    db.collection("ThreatLevels_Tb").document(level_name).delete()
