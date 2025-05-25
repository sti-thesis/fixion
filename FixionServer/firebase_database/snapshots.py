from firebase_admin import firestore

db = firestore.client()

# Create a new Snapshot
def create_snapshot(snapshot_id, machine_id, local_path, cloud_path, snapshot_hash, threat_level_at_creation, size):
    db.collection("Snapshots_Tb").document(snapshot_id).set({
        "machine_id": machine_id,
        "local_path": local_path,
        "cloud_path": cloud_path,
        "snapshot_hash": snapshot_hash,
        "threat_level_at_creation": threat_level_at_creation,
        "created_at": firestore.SERVER_TIMESTAMP,
        "size": size,
        "integrity_status": "",
        "threat_detected": False,
        "is_backed_up": False
    })

# Read a Snapshot by ID
def get_snapshot(snapshot_id):
    doc = db.collection("Snapshots_Tb").document(snapshot_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Snapshot by ID
def update_snapshot(snapshot_id, data):
    db.collection("Snapshots_Tb").document(snapshot_id).update(data)

# Delete a Snapshot by ID
def delete_snapshot(snapshot_id):
    db.collection("Snapshots_Tb").document(snapshot_id).delete()
