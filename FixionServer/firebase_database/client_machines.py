from firebase_admin import firestore

db = firestore.client()

# Create a new Client Machine
def create_client_machine(machine_id, hostname, ip_address, os_version, status):
    db.collection("ClientMachines_Tb").document(machine_id).set({
        "hostname": hostname,
        "ip_address": ip_address,
        "os_version": os_version,
        "status": status,
        "last_check_in": firestore.SERVER_TIMESTAMP
    })

# Read a Client Machine by ID
def get_client_machine(machine_id):
    doc = db.collection("ClientMachines_Tb").document(machine_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Client Machine by ID
def update_client_machine(machine_id, data):
    db.collection("ClientMachines_Tb").document(machine_id).update(data)

# Delete a Client Machine by ID
def delete_client_machine(machine_id):
    db.collection("ClientMachines_Tb").document(machine_id).delete()