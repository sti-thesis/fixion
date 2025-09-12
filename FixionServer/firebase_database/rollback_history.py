from firebase_admin import firestore

db = firestore.client()

# Create a new Rollback History
def create_rollback_history(snapshot_id, machine_id, rollback_reason, restored_by):
    db.collection("RollbackHistory_Tb").document(snapshot_id).set({
        "snapshot_id": snapshot_id,
        "machine_id": machine_id,
        "rollback_reason": rollback_reason,
        "restored_by": restored_by,
        "rollback_timestamp": firestore.SERVER_TIMESTAMP,
        "status": "completed"
    })

# Read a Rollback History by Snapshot ID
def get_rollback_history(snapshot_id):
    doc = db.collection("RollbackHistory_Tb").document(snapshot_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Rollback History by Snapshot ID
def update_rollback_history(snapshot_id, data):
    db.collection("RollbackHistory_Tb").document(snapshot_id).update(data)

# Delete a Rollback History by Snapshot ID
def delete_rollback_history(snapshot_id):
    db.collection("RollbackHistory_Tb").document(snapshot_id).delete()
