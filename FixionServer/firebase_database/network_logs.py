from firebase_admin import firestore

db = firestore.client()

# Create a new Network entry
def create_network(network_id, machine_id, destination_IP, protocol, source_IP, packet_size, detected_anomaly):
    db.collection("NetworkLogs_Tb").document(network_id).set({
        "machine_id": machine_id,
        "destination_IP": destination_IP,
        "packet_size": packet_size,
        "protocol": protocol,
        "source_IP": source_IP ,
        "detected_anomaly": detected_anomaly,
        "time_detected": firestore.SERVER_TIMESTAMP
    })

# Read a Network entry by Network ID
def get_network(network_id):
    doc = db.collection("Network_Tb").document(network_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update a Network entry by Network ID
def update_network(network_id, data):
    db.collection("Network_Tb").document(network_id).update(data)

# Delete a Network entry by Network ID
def delete_network(network_id):
    db.collection("Network_Tb").document(network_id).delete()
