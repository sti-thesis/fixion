from firebase_admin import firestore

db = firestore.client()

# Create a new AI Activity Log
def create_ai_activity_log(machine_ID, threat_id, model_version, action_taken, confidence_score):
    db.collection("AIActivityLogs_Tb").document(threat_id).set({
        "machine_ID": machine_ID,
        "threat_id": threat_id,
        "model_version": model_version,
        "action_taken": action_taken,
        "confidence_score": confidence_score,
        "logged_at": firestore.SERVER_TIMESTAMP
    })

# Read an AI Activity Log by Threat ID
def get_ai_activity_log(threat_id):
    doc = db.collection("AIActivityLogs_Tb").document(threat_id).get
