from firebase_admin import firestore

db = firestore.client()

# Create a new User
def create_user(user_id, username, first_name, last_name, password_hash, role, email):
    db.collection("Users").document(user_id).set({
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "password_hash": password_hash,
        "role": role,
        "email": email,
        "created_at": firestore.SERVER_TIMESTAMP,
        "last_login": firestore.SERVER_TIMESTAMP,
        "is_active": True
    })

# Read a User by ID
def get_user(user_id):
    doc = db.collection("Users").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a User by ID
def update_user(user_id, data):
    db.collection("Users").document(user_id).update(data)

# Delete a User by ID
def delete_user(user_id):
    db.collection("Users").document(user_id).delete()
