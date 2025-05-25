import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed

import ai_scanner


class ScanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Malware Scanner")
        self.geometry("700x450")

        self.create_widgets()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.scan_thread = None
        self.stop_scan_flag = False

    def create_widgets(self):
        # Status label
        self.label_status = tk.Label(self, text="Status: Idle", anchor="w")
        self.label_status.pack(fill=tk.X, padx=10, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self, length=650, mode='determinate')
        self.progress.pack(padx=10, pady=5)

        # Results list with scrollbar
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Consolas", 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_quick = tk.Button(btn_frame, text="Quick Scan", width=15, command=self.start_quick_scan)
        self.btn_quick.grid(row=0, column=0, padx=5)

        self.btn_full = tk.Button(btn_frame, text="Full Scan", width=15, command=self.start_full_scan)
        self.btn_full.grid(row=0, column=1, padx=5)

        self.btn_selective = tk.Button(btn_frame, text="Selective Scan", width=15, command=self.start_selective_scan)
        self.btn_selective.grid(row=0, column=2, padx=5)

        self.btn_stop = tk.Button(btn_frame, text="Stop Scan", width=15, command=self.stop_scan, state=tk.DISABLED)
        self.btn_stop.grid(row=0, column=3, padx=5)

    def update_status(self, text):
        self.label_status.config(text=text)

    def append_result(self, text):
        self.listbox.insert(tk.END, text)
        self.listbox.yview_moveto(1)

    def start_quick_scan(self):
        self.start_scan(path="C:/", quick=True)

    def start_full_scan(self):
        self.start_scan(path="C:/", quick=False)

    def start_selective_scan(self):
        # Open file dialog for selective scan files
        files = filedialog.askopenfilenames(title="Select files for selective scan")
        if not files:
            return
        self.start_scan(path="", quick=False, selective_files=list(files))

    def start_scan(self, path, quick=False, selective_files=None):
        if self.scan_thread and self.scan_thread.is_alive():
            messagebox.showwarning("Scan running", "A scan is already running.")
            return

        self.stop_scan_flag = False
        self.listbox.delete(0, tk.END)
        self.progress['value'] = 0
        self.update_status("Starting scan...")

        # Calculate total files for progress bar
        if selective_files:
            total_files = len(selective_files)
        else:
            total_files = 0
            for _ in ai_scanner.file_generator(path, quick):
                total_files += 1
        self.progress['maximum'] = total_files if total_files > 0 else 1

        def scan_runner():
            scanned_count = 0
            results = []
            lock = threading.Lock()

            def scan_and_report(file_path):
                nonlocal scanned_count
                if self.stop_scan_flag:
                    return None
                self.after(0, lambda: self.update_status(f"Scanning: {file_path} ({scanned_count + 1}/{total_files})"))
                result = ai_scanner.ai_scan(file_path)
                self.after(0, lambda: self.append_result(
                    f"{result['file']} | Action: {result['action']} | Confidence: {result['confidence']:.2f} | Anomaly: {result['anomaly_score']:.4f}"
                ))
                return result

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                files_iter = ai_scanner.file_generator(path, quick, selective_files)
                for file_path in files_iter:
                    if self.stop_scan_flag:
                        break
                    futures.append(executor.submit(scan_and_report, file_path))

                for future in as_completed(futures):
                    if self.stop_scan_flag:
                        break
                    res = future.result()
                    if res:
                        with lock:
                            results.append(res)
                            scanned_count += 1
                            self.after(0, lambda: self.progress.step(1))
                            self.after(0, lambda: self.update_status(f"Scanning files... {scanned_count}/{total_files}"))

            self.after(0, lambda: self.update_status("Scan stopped." if self.stop_scan_flag else "Scan completed."))
            self.after(0, lambda: self.btn_stop.config(state=tk.DISABLED))
            self.after(0, lambda: self.btn_quick.config(state=tk.NORMAL))
            self.after(0, lambda: self.btn_full.config(state=tk.NORMAL))
            self.after(0, lambda: self.btn_selective.config(state=tk.NORMAL))

        # Disable buttons while scanning
        self.btn_quick.config(state=tk.DISABLED)
        self.btn_full.config(state=tk.DISABLED)
        self.btn_selective.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        self.scan_thread = threading.Thread(target=scan_runner, daemon=True)
        self.scan_thread.start()

    def stop_scan(self):
        if messagebox.askyesno("Stop Scan", "Are you sure you want to stop the scan?"):
            self.stop_scan_flag = True
            self.update_status("Stopping scan...")


if __name__ == "__main__":
    app = ScanApp()
    app.mainloop()
