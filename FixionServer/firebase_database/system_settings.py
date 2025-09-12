from firebase_admin import firestore

db = firestore.client()

# Create a new System Setting
def create_system_setting(user_id, config_name, config_value):
    db.collection("SystemSetting_Tb").document(config_name).set({
        "user_id": user_id,
        "config_name": config_name,
        "config_value": config_value,
        "last_updated": firestore.SERVER_TIMESTAMP
    })

# Read a System Setting by Config Name
def get_system_setting(config_name):
    doc = db.collection("SystemSetting_Tb").document(config_name).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a System Setting by Config Name
def update_system_setting(config_name, data):
    db.collection("SystemSetting_Tb").document(config_name).update(data)

# Delete a System Setting by Config Name
def delete_system_setting(config_name):
    db.collection("SystemSetting_Tb").document(config_name).delete()
