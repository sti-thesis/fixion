from firebase_admin import firestore

db = firestore.client()

# Create a new Notification
def create_notification(notification_id, user_id, title, body, machine_id, is_seen):
    db.collection("Notifications_Tb").document(notification_id).set({
        "user_id": user_id,
        "title": title,
        "body": body,
        "machine_id": machine_id,
        "is_seen": is_seen,
        "sent_at": firestore.SERVER_TIMESTAMP
    })

# Read a Notification by Notification ID
def get_notification(notification_id):
    doc = db.collection("Notifications_Tb").document(notification_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Notification by Notification ID
def update_notification(notification_id, data):
    db.collection("Notifications_Tb").document(notification_id).update(data)

# Delete a Notification by Notification ID
def delete_notification(notification_id):
    db.collection("Notifications_Tb").document(notification_id).delete()
