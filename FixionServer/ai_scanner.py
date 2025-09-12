import os
import time
import threading
import psutil
import joblib
import numpy as np
import tensorflow as tf
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# === Paths to Models ===
RF_MODEL_PATH = "rf_hash_model.pkl"
AUTOENCODER_PATH = "unsupervised_autoencoder.keras"
SCALER_PATH = "scaler.pkl"

# === Thresholds ===
CPU_THRESHOLD = 75  # %
ANOMALY_THRESHOLD = 0.05
CONFIDENCE_THRESHOLD = 0.80
QUEUE_MAX_SIZE = 100  # Maximum files in queue at once
MAX_WORKERS = 4

# === Load Models (with error handling) ===
try:
    rf_model = joblib.load(RF_MODEL_PATH)
    autoencoder = load_model(AUTOENCODER_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("[Init] Models loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load models: {e}")
    # Create dummy models for testing
    rf_model = None
    autoencoder = None
    scaler = None

# === Global Variables ===
scan_active = threading.Event()
scan_stats = {
    'total_scanned': 0,
    'threats_found': 0,
    'scanning': False
}
stats_lock = threading.Lock()


# === Decision Support System ===
def dss(anomaly_score, confidence):
    if anomaly_score > 0.05 and confidence < 0.8:
        return "Quarantine"
    elif anomaly_score > 0.1:
        return "Delete"
    elif confidence > 0.95:
        return "Log as Known Malware"
    else:
        return "Monitor"


# === Feature Extraction Placeholder ===
def extract_features(file_path):
    # Replace with actual feature extraction logic
    # For now, return dummy features that match scaler expectations
    if scaler is not None:
        return np.random.rand(scaler.mean_.shape[0])
    else:
        return np.random.rand(50)  # Dummy size


# === AI Scan Engine ===
def ai_scan(file_path):
    try:
        if rf_model is None or autoencoder is None or scaler is None:
            # Dummy scan for testing
            features = np.random.rand(50)
            pred = np.random.choice([0, 1])
            confidence = np.random.rand()
            anomaly_score = np.random.rand() * 0.1
        else:
            features = extract_features(file_path)
            scaled = scaler.transform([features])
            pred = rf_model.predict(scaled)[0]
            confidence = rf_model.predict_proba(scaled).max()
            reconstruction = autoencoder.predict(scaled, verbose=0)
            anomaly_score = np.mean(np.square(scaled - reconstruction))

        decision = dss(anomaly_score, confidence)

        # Update stats
        with stats_lock:
            scan_stats['total_scanned'] += 1
            if decision in ["Quarantine", "Delete", "Log as Known Malware"]:
                scan_stats['threats_found'] += 1

        return {
            "file": file_path,
            "label": pred,
            "confidence": confidence,
            "anomaly_score": anomaly_score,
            "action": decision
        }
    except Exception as e:
        print(f"[ERROR] Scanning {file_path}: {e}")
        return {
            "file": file_path,
            "label": -1,
            "confidence": 0,
            "anomaly_score": 0,
            "action": "Error",
            "error": str(e)
        }


# === File Discovery Worker ===
def file_discovery_worker(path, file_queue, quick=False, selective_files=None):
    """Discovers files and adds them to queue without blocking"""
    try:
        if selective_files:
            for file_path in selective_files:
                if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                    file_queue.put(file_path)
                    print(f"[Queued] {file_path}")
                else:
                    print(f"[Skip] Cannot access {file_path}")
        else:
            for root, _, files in os.walk(path, topdown=True):
                if not scan_active.is_set():
                    break

                for file_name in files:
                    if not scan_active.is_set():
                        break

                    full_path = os.path.join(root, file_name)

                    # Quick scan filter
                    if quick and not full_path.lower().endswith(
                            ('.exe', '.dll', '.bat', '.cmd', '.scr', '.com', '.pif')):
                        continue

                    if os.path.isfile(full_path) and os.access(full_path, os.R_OK):
                        # Wait if queue is full to prevent memory issues
                        while file_queue.qsize() >= QUEUE_MAX_SIZE and scan_active.is_set():
                            time.sleep(0.1)

                        if scan_active.is_set():
                            file_queue.put(full_path)
                            print(f"[Queued] {full_path}")

    except Exception as e:
        print(f"[ERROR] File discovery: {e}")
    finally:
        # Signal that file discovery is complete
        file_queue.put(None)  # Sentinel value
        print("[Discovery] File discovery completed")


# === Scan Worker ===
def scan_worker(file_queue, results_queue):
    """Worker thread that processes files from queue"""
    while scan_active.is_set():
        try:
            # Get file from queue with timeout
            file_path = file_queue.get(timeout=1)

            # Check for sentinel value (end of discovery)
            if file_path is None:
                file_queue.put(None)  # Re-queue sentinel for other workers
                break

            print(f"[Scanning] {file_path}")
            result = ai_scan(file_path)
            results_queue.put(result)
            print(f"[Result] {file_path}: Action = {result['action']}")

            file_queue.task_done()

        except Empty:
            # No files in queue, continue waiting
            continue
        except Exception as e:
            print(f"[ERROR] Scan worker: {e}")


# === Results Processor ===
def results_processor(results_queue, results_list):
    """Processes scan results without blocking main thread"""
    while scan_active.is_set():
        try:
            result = results_queue.get(timeout=1)
            results_list.append(result)
            results_queue.task_done()
        except Empty:
            continue
        except Exception as e:
            print(f"[ERROR] Results processor: {e}")


# === Main Scan Function ===
def scan_directory(path, quick=False, selective_files=None, max_workers=MAX_WORKERS):
    """Main scanning function with queue-based architecture"""
    print(f"[Scan Start] {path} ({'Quick' if quick else 'Full'})")

    # Reset stats
    with stats_lock:
        scan_stats.update({
            'total_scanned': 0,
            'threats_found': 0,
            'scanning': True
        })

    # Create queues
    file_queue = Queue(maxsize=QUEUE_MAX_SIZE)
    results_queue = Queue()
    results_list = []

    # Set scan active flag
    scan_active.set()

    try:
        # Start file discovery thread
        discovery_thread = threading.Thread(
            target=file_discovery_worker,
            args=(path, file_queue, quick, selective_files),
            daemon=True
        )
        discovery_thread.start()

        # Start scan workers
        scan_threads = []
        for i in range(max_workers):
            thread = threading.Thread(
                target=scan_worker,
                args=(file_queue, results_queue),
                daemon=True
            )
            thread.start()
            scan_threads.append(thread)

        # Start results processor
        results_thread = threading.Thread(
            target=results_processor,
            args=(results_queue, results_list),
            daemon=True
        )
        results_thread.start()

        # Wait for discovery to complete
        discovery_thread.join()

        # Wait for all files to be processed
        file_queue.join()

        # Wait for all results to be processed
        results_queue.join()

        # Wait for scan threads to finish
        for thread in scan_threads:
            thread.join(timeout=5)

    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Scan cancelled by user")
    except Exception as e:
        print(f"[ERROR] Scan error: {e}")
    finally:
        # Clean shutdown
        scan_active.clear()
        with stats_lock:
            scan_stats['scanning'] = False

    print(f"[Scan Complete] Scanned {len(results_list)} files. Threats found: {scan_stats['threats_found']}")
    return results_list


# === Background Scanner ===
def background_scanner():
    """Background scanning with CPU monitoring"""
    print("[Init] Background scanner running...")
    while True:
        try:
            # Check CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > CPU_THRESHOLD:
                print(f"[Background] High CPU usage ({cpu_usage}%). Waiting...")
                time.sleep(10)
                continue

            # Check if another scan is running
            if scan_stats['scanning']:
                print("[Background] Another scan is running. Waiting...")
                time.sleep(30)
                continue

            print("[Background] Starting background scan...")
            scan_directory("C:/", quick=True, max_workers=2)  # Use fewer workers for background

            # Wait before next background scan
            time.sleep(300)  # 5 minutes

        except Exception as e:
            print(f"[ERROR] Background scanner: {e}")
            time.sleep(60)


# === Launch Background Thread ===
def start_background_scanner():
    """Start background scanning thread"""
    bg_thread = threading.Thread(target=background_scanner, daemon=True)
    bg_thread.start()
    print("[Init] Background scanner started.")


# === Manual Scanning Options ===
def manual_quick_scan():
    """Perform manual quick scan"""
    return scan_directory("C:/", quick=True)


def manual_full_scan():
    """Perform manual full scan"""
    return scan_directory("C:/", quick=False)


def manual_selective_scan(file_list):
    """Perform selective scan on specific files"""
    return scan_directory("", quick=False, selective_files=file_list)


def get_scan_stats():
    """Get current scan statistics"""
    with stats_lock:
        return scan_stats.copy()


def stop_scan():
    """Stop current scan"""
    scan_active.clear()
    print("[Manual] Scan stop requested")


# === Example Usage ===
if __name__ == "__main__":
    print("=== AI Antivirus Scanner ===")

    # Start background scanner
    start_background_scanner()

    # Wait a bit for initialization
    time.sleep(2)

    try:
        while True:
            print("\n=== Menu ===")
            print("1. Quick Scan")
            print("2. Full Scan")
            print("3. Selective Scan")
            print("4. Show Stats")
            print("5. Stop Current Scan")
            print("6. Exit")

            choice = input("Choose option (1-6): ").strip()

            if choice == '1':
                print("\n--- Starting Quick Scan ---")
                results = manual_quick_scan()
                print(f"Quick scan completed. {len(results)} files processed.")

            elif choice == '2':
                print("\n--- Starting Full Scan ---")
                results = manual_full_scan()
                print(f"Full scan completed. {len(results)} files processed.")

            elif choice == '3':
                files = input("Enter file paths (comma-separated): ").strip().split(',')
                files = [f.strip() for f in files if f.strip()]
                if files:
                    print(f"\n--- Starting Selective Scan on {len(files)} files ---")
                    results = manual_selective_scan(files)
                    print(f"Selective scan completed. {len(results)} files processed.")
                else:
                    print("No valid files provided.")

            elif choice == '4':
                stats = get_scan_stats()
                print(f"\n--- Scan Statistics ---")
                print(f"Total Scanned: {stats['total_scanned']}")
                print(f"Threats Found: {stats['threats_found']}")
                print(f"Currently Scanning: {stats['scanning']}")

            elif choice == '5':
                stop_scan()

            elif choice == '6':
                print("Exiting...")
                stop_scan()
                break

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_scan()