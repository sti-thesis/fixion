from firebase_admin import firestore

db = firestore.client()

# Create a new Cloud Backup
def create_cloud_backup(user_id, machine_id, snapshot_id, backup_location, backup_type):
    db.collection("CloudBackup_Tb").document(snapshot_id).set({
        "user_id": user_id,
        "machine_id": machine_id,
        "snapshot_id": snapshot_id,
        "backup_timestamp": firestore.SERVER_TIMESTAMP,
        "backup_location": backup_location,
        "backup_type": backup_type,
        "status": "completed"
    })

# Read a Cloud Backup by Snapshot ID
def get_cloud_backup(snapshot_id):
    doc = db.collection("CloudBackup_Tb").document(snapshot_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Cloud Backup by Snapshot ID
def update_cloud_backup(snapshot_id, data):
    db.collection("CloudBackup_Tb").document(snapshot_id).update(data)

# Delete a Cloud Backup by Snapshot ID
def delete_cloud_backup(snapshot_id):
    db.collection("CloudBackup_Tb").document(snapshot_id).delete()
