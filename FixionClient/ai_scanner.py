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
from typing import Callable, Optional, List, Dict, Any

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


class AIAntivirusScanner:
    def __init__(self):
        self.rf_model = None
        self.autoencoder = None
        self.scaler = None

        # Threading controls
        self.scan_active = threading.Event()
        self.stats_lock = threading.Lock()

        # Statistics
        self.scan_stats = {
            'total_scanned': 0,
            'threats_found': 0,
            'scanning': False,
            'current_file': '',
            'scan_type': '',
            'start_time': None,
            'estimated_files': 0,
            'background_active': True,  # Always active by default
            'last_background_scan': None,
            'background_scans_completed': 0
        }

        # Callbacks for dashboard integration
        self.file_scanned_callback = None
        self.progress_callback = None
        self.status_callback = None
        self.result_callback = None

        # Background scanner thread
        self.background_thread = None

        # Load models
        self._load_models()

        # Auto-start background scanner
        self.start_background_scanner()

    def _load_models(self):
        """Load ML models with error handling"""
        try:
            self.rf_model = joblib.load(RF_MODEL_PATH)
            self.autoencoder = load_model(AUTOENCODER_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            self._update_status("Models loaded successfully")
        except Exception as e:
            self._update_status(f"Failed to load models: {e}")
            # Create dummy models for testing
            self.rf_model = None
            self.autoencoder = None
            self.scaler = None

    def _update_status(self, message: str):
        """Update status via callback"""
        if self.status_callback:
            self.status_callback(message)
        print(f"[Status] {message}")

    def _update_progress(self, current: int, total: int, current_file: str = ""):
        """Update progress via callback"""
        with self.stats_lock:
            self.scan_stats['current_file'] = current_file

        if self.progress_callback:
            self.progress_callback(current, total, current_file)

    def _notify_file_scanned(self, file_path: str, result: Dict[str, Any]):
        """Notify dashboard of scanned file"""
        if self.file_scanned_callback:
            self.file_scanned_callback(file_path, result)

        if self.result_callback and result['action'] in ["Quarantine", "Delete", "Log as Known Malware"]:
            self.result_callback(result)

    def set_callbacks(self,
                      file_scanned_callback: Optional[Callable] = None,
                      progress_callback: Optional[Callable] = None,
                      status_callback: Optional[Callable] = None,
                      result_callback: Optional[Callable] = None):
        """Set callbacks for dashboard integration"""
        self.file_scanned_callback = file_scanned_callback
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.result_callback = result_callback

    def dss(self, anomaly_score: float, confidence: float) -> str:
        """Decision Support System"""
        if anomaly_score > 0.05 and confidence < 0.8:
            return "Quarantine"
        elif anomaly_score > 0.1:
            return "Delete"
        elif confidence > 0.95:
            return "Log as Known Malware"
        else:
            return "Monitor"

    def extract_features(self, file_path: str) -> np.ndarray:
        """Extract features from file (placeholder implementation)"""
        # Replace with actual feature extraction logic
        if self.scaler is not None:
            return np.random.rand(self.scaler.mean_.shape[0])
        else:
            return np.random.rand(50)  # Dummy size

    def ai_scan(self, file_path: str) -> Dict[str, Any]:
        """AI scan engine"""
        try:
            if self.rf_model is None or self.autoencoder is None or self.scaler is None:
                # Dummy scan for testing
                features = np.random.rand(50)
                pred = np.random.choice([0, 1])
                confidence = np.random.rand()
                anomaly_score = np.random.rand() * 0.1
            else:
                features = self.extract_features(file_path)
                scaled = self.scaler.transform([features])
                pred = self.rf_model.predict(scaled)[0]
                confidence = self.rf_model.predict_proba(scaled).max()
                reconstruction = self.autoencoder.predict(scaled, verbose=0)
                anomaly_score = np.mean(np.square(scaled - reconstruction))

            decision = self.dss(anomaly_score, confidence)

            # Update stats
            with self.stats_lock:
                self.scan_stats['total_scanned'] += 1
                if decision in ["Quarantine", "Delete", "Log as Known Malware"]:
                    self.scan_stats['threats_found'] += 1

            return {
                "file": file_path,
                "label": pred,
                "confidence": confidence,
                "anomaly_score": anomaly_score,
                "action": decision,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "file": file_path,
                "label": -1,
                "confidence": 0,
                "anomaly_score": 0,
                "action": "Error",
                "error": str(e),
                "timestamp": time.time()
            }

    def _estimate_files(self, path: str, quick: bool = False) -> int:
        """Estimate number of files to scan"""
        count = 0
        try:
            for root, _, files in os.walk(path):
                for file_name in files:
                    if quick and not file_name.lower().endswith(
                            ('.exe', '.dll', '.bat', '.cmd', '.scr', '.com', '.pif')):
                        continue
                    count += 1
                    if count > 10000:  # Cap estimation for performance
                        return count
        except Exception:
            pass
        return count

    def file_discovery_worker(self, path: str, file_queue: Queue, quick: bool = False,
                              selective_files: Optional[List[str]] = None):
        """Discovers files and adds them to queue"""
        try:
            if selective_files:
                for file_path in selective_files:
                    if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                        file_queue.put(file_path)
                    else:
                        self._update_status(f"Cannot access {file_path}")
            else:
                for root, _, files in os.walk(path, topdown=True):
                    if not self.scan_active.is_set():
                        break

                    for file_name in files:
                        if not self.scan_active.is_set():
                            break

                        full_path = os.path.join(root, file_name)

                        # Quick scan filter
                        if quick and not full_path.lower().endswith(
                                ('.exe', '.dll', '.bat', '.cmd', '.scr', '.com', '.pif')):
                            continue

                        if os.path.isfile(full_path) and os.access(full_path, os.R_OK):
                            # Wait if queue is full to prevent memory issues
                            while file_queue.qsize() >= QUEUE_MAX_SIZE and self.scan_active.is_set():
                                time.sleep(0.1)

                            if self.scan_active.is_set():
                                file_queue.put(full_path)

        except Exception as e:
            self._update_status(f"File discovery error: {e}")
        finally:
            # Signal that file discovery is complete
            file_queue.put(None)  # Sentinel value

    def scan_worker(self, file_queue: Queue, results_queue: Queue):
        """Worker thread that processes files from queue"""
        while self.scan_active.is_set():
            try:
                # Get file from queue with timeout
                file_path = file_queue.get(timeout=1)

                # Check for sentinel value (end of discovery)
                if file_path is None:
                    file_queue.put(None)  # Re-queue sentinel for other workers
                    break

                # Update progress
                with self.stats_lock:
                    current = self.scan_stats['total_scanned']
                    total = self.scan_stats['estimated_files']
                    self._update_progress(current, total, file_path)

                # Scan file
                result = self.ai_scan(file_path)
                results_queue.put(result)

                # Notify dashboard
                self._notify_file_scanned(file_path, result)

                file_queue.task_done()

            except Empty:
                # No files in queue, continue waiting
                continue
            except Exception as e:
                self._update_status(f"Scan worker error: {e}")

    def results_processor(self, results_queue: Queue, results_list: List[Dict[str, Any]]):
        """Processes scan results"""
        while self.scan_active.is_set():
            try:
                result = results_queue.get(timeout=1)
                results_list.append(result)
                results_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                self._update_status(f"Results processor error: {e}")

    def scan_directory(self, path: str, quick: bool = False,
                       selective_files: Optional[List[str]] = None,
                       max_workers: int = MAX_WORKERS) -> List[Dict[str, Any]]:
        """Main scanning function"""
        scan_type = "Quick" if quick else "Full"
        if selective_files:
            scan_type = "Selective"

        self._update_status(f"Starting {scan_type} scan of {path}")

        # Reset stats
        with self.stats_lock:
            self.scan_stats.update({
                'total_scanned': 0,
                'threats_found': 0,
                'scanning': True,
                'current_file': '',
                'scan_type': scan_type,
                'start_time': time.time(),
                'estimated_files': len(selective_files) if selective_files else self._estimate_files(path, quick)
            })

        # Create queues
        file_queue = Queue(maxsize=QUEUE_MAX_SIZE)
        results_queue = Queue()
        results_list = []

        # Set scan active flag
        self.scan_active.set()

        try:
            # Start file discovery thread
            discovery_thread = threading.Thread(
                target=self.file_discovery_worker,
                args=(path, file_queue, quick, selective_files),
                daemon=True
            )
            discovery_thread.start()

            # Start scan workers
            scan_threads = []
            for i in range(max_workers):
                thread = threading.Thread(
                    target=self.scan_worker,
                    args=(file_queue, results_queue),
                    daemon=True
                )
                thread.start()
                scan_threads.append(thread)

            # Start results processor
            results_thread = threading.Thread(
                target=self.results_processor,
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
            self._update_status("Scan cancelled by user")
        except Exception as e:
            self._update_status(f"Scan error: {e}")
        finally:
            # Clean shutdown
            self.scan_active.clear()
            with self.stats_lock:
                self.scan_stats['scanning'] = False
                scan_time = time.time() - self.scan_stats['start_time']

            self._update_status(
                f"Scan completed: {len(results_list)} files in {scan_time:.1f}s. Threats: {self.scan_stats['threats_found']}")

        return results_list

    def background_scanner(self):
        """Background scanning with CPU monitoring - runs continuously"""
        self._update_status("Background protection active")
        while True:
            try:
                # Always run background scanning (no toggle check)

                # Check CPU usage
                cpu_usage = psutil.cpu_percent(interval=1)
                if cpu_usage > CPU_THRESHOLD:
                    # Don't show repeated CPU messages, just wait
                    time.sleep(10)
                    continue

                # Check if manual scan is running
                if self.scan_stats['scanning']:
                    time.sleep(30)
                    continue

                # Perform background scan
                with self.stats_lock:
                    self.scan_stats['last_background_scan'] = time.time()

                self._update_status("Performing background scan...")
                self.scan_directory("C:/", quick=True, max_workers=2)

                with self.stats_lock:
                    self.scan_stats['background_scans_completed'] += 1

                self._update_status("Background protection active")

                # Wait before next background scan
                time.sleep(300)  # 5 minutes

            except Exception as e:
                self._update_status(f"Background scanner error: {e}")
                time.sleep(60)  # Wait before retrying

    def start_background_scanner(self):
        """Start background scanning thread (auto-started on init)"""
        if self.background_thread is None or not self.background_thread.is_alive():
            self.background_thread = threading.Thread(target=self.background_scanner, daemon=True)
            self.background_thread.start()
            self._update_status("Real-time protection enabled")

    def get_background_status(self) -> Dict[str, Any]:
        """Get background scanning status information"""
        with self.stats_lock:
            return {
                'active': self.scan_stats['background_active'],
                'last_scan': self.scan_stats['last_background_scan'],
                'scans_completed': self.scan_stats['background_scans_completed'],
                'thread_alive': self.background_thread.is_alive() if self.background_thread else False
            }

    def quick_scan(self, path: str = "C:/") -> List[Dict[str, Any]]:
        """Perform quick scan"""
        return self.scan_directory(path, quick=True)

    def full_scan(self, path: str = "C:/") -> List[Dict[str, Any]]:
        """Perform full scan"""
        return self.scan_directory(path, quick=False)

    def selective_scan(self, file_list: List[str]) -> List[Dict[str, Any]]:
        """Perform selective scan on specific files"""
        return self.scan_directory("", quick=False, selective_files=file_list)

    def get_scan_stats(self) -> Dict[str, Any]:
        """Get current scan statistics"""
        with self.stats_lock:
            stats = self.scan_stats.copy()
            if stats['start_time']:
                stats['elapsed_time'] = time.time() - stats['start_time']
            return stats

    def stop_scan(self):
        """Stop current scan"""
        self.scan_active.clear()
        self._update_status("Scan stop requested")

    def is_scanning(self) -> bool:
        """Check if currently scanning"""
        return self.scan_stats['scanning']