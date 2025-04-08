import os
import shutil
import datetime
import zipfile
import schedule
import time
import threading
import tempfile
import filecmp

SNAPSHOT_DIR = "snapshots"
TARGET_DIR = "system_files"

#CREATING SNAPSHOT
def create_snapshot(snapshot_name: str) -> bool:
    try:
        # Make sure the snapshots folder exists
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)

        # Generate a filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_filename = f"{snapshot_name}_{timestamp}.zip"
        snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_filename)

        # Zip everything inside the system_files folder
        with zipfile.ZipFile(snapshot_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(TARGET_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, TARGET_DIR)
                    zipf.write(file_path, arcname)

        print(f"Snapshot saved to {snapshot_path}")
        return True

    except Exception as e:
        print(f"Snapshot creation failed: {e}")
        return False

#FOR TESTING (remove the hashtag)
#if __name__ == "__main__":
    #create_snapshot("test_snapshot")

#RESTORE SNAPSHOT
def restore_snapshot(snapshot_name: str) -> bool:
    try:
        # Build full path to the snapshot zip file
        snapshot_path = os.path.join("snapshots", snapshot_name)

        if not os.path.exists(snapshot_path):
            print(f"Snapshot '{snapshot_name}' not found.")
            return False

        # Step 1: Clean current system_files folder
        if os.path.exists(TARGET_DIR):
            shutil.rmtree(TARGET_DIR)  # Delete current system files
        os.makedirs(TARGET_DIR)  # Recreate empty folder

        # Step 2: Extract the snapshot
        with zipfile.ZipFile(snapshot_path, 'r') as zipf:
            zipf.extractall(TARGET_DIR)

        print(f"System restored from {snapshot_path}")
        return True

    except Exception as e:
        print(f"Snapshot restoration failed: {e}")
        return False

#FOR TESTING (remove hashtags)
#if __name__ == "__main__":
    # Test restoring
   # snapshots = os.listdir("snapshots")
   # if snapshots:
     #   print(f"Found snapshots: {snapshots}")
     #   restore_snapshot(snapshots[0])  # Try restoring the first snapshot
   # else:
      #  print("No snapshots found.")

#LISTING OF SNAPSHOTS
def list_snapshots() -> list:
    try:
        snapshots_list = []

        if not os.path.exists(SNAPSHOT_DIR):
            print("No snapshot directory found.")
            return []

        for filename in os.listdir(SNAPSHOT_DIR):
            if filename.endswith(".zip"):
                file_path = os.path.join(SNAPSHOT_DIR, filename)

                # Get file info
                size_bytes = os.path.getsize(file_path)
                size_mb = round(size_bytes / (1024 * 1024), 2)
                modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

                # Extract snapshot name (remove .zip and timestamp if desired)
                snapshots_list.append({
                    "filename": filename,
                    "timestamp": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "size_mb": size_mb
                })

        return snapshots_list

    except Exception as e:
        print(f"Failed to list snapshots: {e}")
        return []

#FOR TESTING (remove hashtags)
#if __name__ == "__main__":
 #   print("Listing snapshots:")
  #  for snap in list_snapshots():
   #     print(f"- {snap['filename']} | {snap['timestamp']} | {snap['size_mb']} MB")

#FOR DELETING SNAPSHOTS
def delete_snapshot(snapshot_name: str) -> bool:
    try:
        snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

        if not os.path.exists(snapshot_path):
            print(f"Snapshot '{snapshot_name}' not found.")
            return False

        os.remove(snapshot_path)
        print(f"Snapshot '{snapshot_name}' deleted.")
        return True

    except Exception as e:
        print(f"Failed to delete snapshot: {e}")
        return False

#FOR TESTING (remove hashtags)
#if __name__ == "__main__":
    # List snapshots first
 #   all_snaps = list_snapshots()
  #  if all_snaps:
   #     print("Available snapshots:")
    #    for snap in all_snaps:
     #       print(f"- {snap['filename']}")

        # Try deleting the first one
      #  to_delete = all_snaps[0]['filename']
       # confirm = input(f"\nDo you want to delete '{to_delete}'? (y/n): ")
        #if confirm.lower() == 'y':
         #   delete_snapshot(to_delete)
        #else:
         #   print("Deletion canceled.")
    #else:
     #   print("No snapshots to delete.")

#SNYCING FIREBASE (wala akong firebase hehe)
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': '<your-bucket-name>.appspot.com'  # Replace with your Firebase Storage bucket
    })

def sync_snapshot_to_cloud(snapshot_name: str) -> bool:
    try:
        snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

        if not os.path.exists(snapshot_path):
            print(f"Snapshot '{snapshot_name}' does not exist.")
            return False

        bucket = storage.bucket()
        blob = bucket.blob(f"snapshots/{snapshot_name}")

        blob.upload_from_filename(snapshot_path)
        blob.make_public()  # Optional: make the file public
        print(f"Snapshot uploaded to Firebase: {blob.public_url}")
        return True

    except Exception as e:
        print(f"Failed to upload snapshot: {e}")
        return False

#FOR TESTING (remove hashtags) (diko pa natry since wala akong firebase hehe labyu gel)
#if __name__ == "__main__":
 #   snaps = list_snapshots()
  #  if snaps:
   #     file_to_upload = snaps[0]['filename']
    #    print(f"Uploading {file_to_upload} to Firebase...")
     #   sync_snapshot_to_cloud(file_to_upload)
   # else:
    #    print("No snapshots found to upload.")

#DOWNLOADING FROM FIREBASE
from firebase_admin import storage

def download_snapshot_from_cloud(snapshot_name: str) -> bool:
    try:
        local_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

        # Create snapshots directory if missing
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)

        bucket = storage.bucket()
        blob = bucket.blob(f"snapshots/{snapshot_name}")

        if not blob.exists():
            print(f"Snapshot '{snapshot_name}' not found in cloud.")
            return False

        blob.download_to_filename(local_path)
        print(f"Snapshot '{snapshot_name}' downloaded to {local_path}")
        return True

    except Exception as e:
        print(f"Download failed: {e}")
        return False

#FOR TESTING (remove hashtags)
#if __name__ == "__main__":
  #  snapshot_to_get = "test_snapshot_20250406_150000.zip"
   # download_snapshot_from_cloud(snapshot_to_get)

#VERIFYING SNAPSHOT INTEG
import hashlib

def verify_snapshot_integrity(snapshot_name: str) -> bool:
    try:
        snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

        if not os.path.exists(snapshot_path):
            print(f"Snapshot '{snapshot_name}' not found.")
            return False

        # Calculate SHA256 hash
        sha256_hash = hashlib.sha256()
        with open(snapshot_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        hash_value = sha256_hash.hexdigest()

        # Optional: Save known-good hash to a .hash file
        hash_file = snapshot_path + ".hash"
        if os.path.exists(hash_file):
            with open(hash_file, "r") as f:
                known_hash = f.read().strip()
            if hash_value == known_hash:
                print("Snapshot integrity verified ✅")
                return True
            else:
                print("Snapshot hash mismatch ❌")
                return False
        else:
            # Save this hash as the reference
            with open(hash_file, "w") as f:
                f.write(hash_value)
            print("Reference hash saved.")
            return True

    except Exception as e:
        print(f"Integrity check failed: {e}")
        return False

#FOR TESTING (remove hashtags pagod na ko)
#if __name__ == "__main__":
 #   verify_snapshot_integrity("test_snapshot_20250406_150000.zip")

#AUTO ROLL BACK TRIGGER
def auto_rollback_trigger(threat_level: str) -> None:
    threat_level = threat_level.lower()

    # Step 1: Get the latest snapshot
    snapshots = list_snapshots()
    if not snapshots:
        print("⚠️ No snapshots available for rollback.")
        return

    # Sort snapshots by timestamp (most recent last)
    snapshots_sorted = sorted(
        snapshots,
        key=lambda x: datetime.datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"),
        reverse=True
    )

    latest_snapshot = snapshots_sorted[0]['filename']

    # Step 2: Decide based on threat level
    if threat_level == "suspicious":
        print("🚨 Suspicious activity detected! No rollback, just logging.")
        log_rollback_event(latest_snapshot, "Suspicious threat detected (monitoring only)")

    elif threat_level == "malicious":
        print("❗Malicious threat detected! Rolling back immediately.")
        success = restore_snapshot(latest_snapshot)
        if success:
            log_rollback_event(latest_snapshot, "Automatic rollback triggered due to malicious threat.")
        else:
            print("❌ Rollback failed.")
    else:
        print(f"Unknown threat level: '{threat_level}' — no action taken.")

#LOGGING FUNCTION
def log_rollback_event(snapshot_name: str, reason: str) -> None:
    try:
        os.makedirs("logs", exist_ok=True)
        log_file = os.path.join("logs", "rollback.log")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] Snapshot: {snapshot_name} | Reason: {reason}\n")

        print("📜 Rollback event logged.")
    except Exception as e:
        print(f"Failed to log rollback: {e}")

#FOR TESTING (REMOVE HASHTAGS HUHU)
#if __name__ == "__main__":
 #   auto_rollback_trigger("suspicious")  # or "malicious"

#SCHEDULE PERIODIC SNAPSHOTS
def schedule_periodic_snapshots(interval_minutes: int) -> None:
    def job():
        # Generate a timestamped snapshot name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"auto_snapshot_{timestamp}"
        print(f"\n🕒 Creating periodic snapshot: {snapshot_name}")
        success = create_snapshot(snapshot_name)
        if success:
            print(f"✅ Snapshot '{snapshot_name}' created successfully.")
        else:
            print(f"❌ Failed to create snapshot '{snapshot_name}'.")

    # Schedule the job every X minutes
    schedule.every(interval_minutes).minutes.do(job)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Run scheduling in background thread
    print(f"📅 Scheduling automatic snapshots every {interval_minutes} minute(s).")
    threading.Thread(target=run_schedule, daemon=True).start()

#FOR TESTING (REMOVE HASHTAAAAGGZZZ)
#if __name__ == "__main__":
 #   schedule_periodic_snapshots(1)  # every 1 minute

  #  print("🛡 System is running... Press Ctrl+C to stop.")
   # try:
    #    while True:
     #       time.sleep(10)
   # except KeyboardInterrupt:
    #    print("\n🛑 Scheduler stopped.")

#GETTING SNAPSHOT METADATA
def get_snapshot_metadata(snapshot_name: str) -> dict:
    snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

    if not os.path.exists(snapshot_path):
        print(f"Snapshot '{snapshot_name}' not found.")
        return {}

    try:
        # File size in KB or MB
        size_bytes = os.path.getsize(snapshot_path)
        size_str = (
            f"{size_bytes / (1024 * 1024):.2f} MB"
            if size_bytes > 1024 * 1024
            else f"{size_bytes / 1024:.2f} KB"
        )

        # Created date
        created_timestamp = os.path.getmtime(snapshot_path)
        created_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_timestamp))

        # Count files in zip
        with zipfile.ZipFile(snapshot_path, 'r') as zipf:
            file_list = zipf.namelist()
            file_count = len(file_list)

        return {
            "snapshot_name": snapshot_name,
            "created_date": created_date,
            "size": size_str,
            "file_count": file_count,
        }

    except Exception as e:
        print(f"Error reading snapshot metadata: {e}")
        return {}

#FOR TESTING (ALAM MO NA)
#if __name__ == "__main__":
 #   snaps = list_snapshots()
  #  if snaps:
   #     sample = snaps[0]["filename"]
    #    print(f"\n📂 Getting metadata for: {sample}")
     #   metadata = get_snapshot_metadata(sample)
      #  print(metadata)
   # else:
    #    print("No snapshots found.")

#COMPARING SNAPSHOTS
def compute_file_hash(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def compare_snapshot_to_current(snapshot_name: str) -> list:
    differences = []
    snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

    if not os.path.exists(snapshot_path):
        print(f"Snapshot '{snapshot_name}' not found.")
        return differences

    try:
        # Step 1: Extract ZIP to a temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(snapshot_path, "r") as zipf:
                zipf.extractall(temp_dir)

            # Step 2: Walk through snapshot files
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), temp_dir)
                    snapshot_file_path = os.path.join(root, file)
                    current_file_path = os.path.join(".", rel_path)

                    # File missing in current system
                    if not os.path.exists(current_file_path):
                        differences.append(f"Missing in current: {rel_path}")
                    else:
                        # Compare hashes
                        snapshot_hash = compute_file_hash(snapshot_file_path)
                        current_hash = compute_file_hash(current_file_path)

                        if snapshot_hash != current_hash:
                            differences.append(f"Modified file: {rel_path}")

            # Step 3: Check for new files added *after* snapshot
            for root, _, files in os.walk("."):
                for file in files:
                    current_rel_path = os.path.relpath(os.path.join(root, file), ".")
                    snapshot_file_path = os.path.join(temp_dir, current_rel_path)
                    if not os.path.exists(snapshot_file_path):
                        differences.append(f"New file not in snapshot: {current_rel_path}")

    except Exception as e:
        print(f"Error comparing snapshot: {e}")

    return differences

#FOR TESTING (YEHEY LAST NA)
#if __name__ == "__main__":
 #   snaps = list_snapshots()
  #  if snaps:
   #     sample = snaps[0]["filename"]
    #    print(f"\n🧠 Comparing snapshot: {sample}")
     #   diff = compare_snapshot_to_current(sample)
      #  if diff:
       #     print("🔍 Differences found:")
        #    for d in diff:
         #       print(" -", d)
       # else:
        #    print("✅ No differences. System matches snapshot.")

