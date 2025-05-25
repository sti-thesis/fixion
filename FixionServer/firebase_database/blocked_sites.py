from firebase_admin import firestore

db = firestore.client()

# Create a new Blocked Site
def create_blocked_site(url, added_by):
    db.collection("BlockedSites_Tb").document(url).set({
        "url": url,
        "added_by": added_by,
        "added_at": firestore.SERVER_TIMESTAMP
    })

# Read a Blocked Site by URL
def get_blocked_site(url):
    doc = db.collection("BlockedSites_Tb").document(url).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Blocked Site by URL
def update_blocked_site(url, data):
    db.collection("BlockedSites_Tb").document(url).update(data)

# Delete a Blocked Site by URL
def delete_blocked_site(url):
    db.collection("BlockedSites_Tb").document(url).delete()
