from calendar import calendar
import calendar as cal_module

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import random
from datetime import datetime, timedelta
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FixionDashboard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Fixion Dashboard")

        # Fixed window size - no resizing, no scrolling
        self.root.geometry("1200x700")
        self.root.configure(fg_color="#14151b")

        # Variables for scan functionality
        self.scanning = False
        self.scan_progress = 0
        self.current_file = ""
        self.files_scanned = 0
        self.total_files = 0
        self.scan_type = "Quick Scan"
        self.selected_scan_path = ""
        self.scan_threats_found = []

        # Sample data
        self.threats = [
            {"name": "Trojan.Generic.KD.123456", "status": "Quarantined", "severity": "High"},
            {"name": "Adware.BrowserModifier", "status": "Removed", "severity": "Medium"},
            {"name": "PUP.Optional.Download", "status": "Detected", "severity": "Low"}
        ]

        self.setup_ui()
        self.update_system_metrics()

    def center_window(self):
        """Center the window on the screen"""
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get window dimensions
        window_width = 1366
        window_height = 768

        # Calculate position coordinates
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set window position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_ui(self):
        # Main container - no scrolling, fixed layout
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure grid weights for the 3x2 layout plus center
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(2, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Create the layout according to your image
        self.create_system_health(self.main_container)  # Top-left
        self.create_network_health(self.main_container)  # Top-right
        self.create_threats_panel(self.main_container)  # Bottom-left
        self.create_scan_center(self.main_container)  # Center (scan button)
        self.create_rollback_panel(self.main_container)  # Bottom-right

    def create_system_health(self, parent):
        """Top-left panel - System Health"""
        system_frame = ctk.CTkFrame(parent, fg_color="#132a3f", border_width=0, corner_radius=18)
        system_frame.grid(row=0, column=0, sticky="nsew", padx=(14, 14), pady=(14, 14))

        title = ctk.CTkLabel(system_frame, text="System Health", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(8, 8))

        # Metrics container
        metrics_container = ctk.CTkFrame(system_frame, fg_color="transparent", border_width=0)
        metrics_container.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        # CPU Usage
        cpu_frame = ctk.CTkFrame(metrics_container, fg_color="transparent", corner_radius=16, height=80)
        cpu_frame.pack(fill="x", pady=(0,7))
        cpu_frame.pack_propagate(False)

        ctk.CTkLabel(cpu_frame, text="CPU Usage", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(0, 0))
        self.cpu_progress = ctk.CTkProgressBar(cpu_frame, width=200, height=12, progress_color="#f59e0b")
        self.cpu_progress.pack(pady=0)
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="45%", font=ctk.CTkFont(size=14, weight="bold"),
                                      text_color="#f59e0b")
        self.cpu_label.pack(pady=(0, 0))

        # Memory Usage
        mem_frame = ctk.CTkFrame(metrics_container, fg_color="transparent", corner_radius=16, height=80)
        mem_frame.pack(fill="x", pady=(0,7))
        mem_frame.pack_propagate(False)

        ctk.CTkLabel(mem_frame, text="Memory Usage", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(4, 4))
        self.mem_progress = ctk.CTkProgressBar(mem_frame, width=200, height=12, progress_color="#3b82f6")
        self.mem_progress.pack(pady=2)
        self.mem_label = ctk.CTkLabel(mem_frame, text="68%", font=ctk.CTkFont(size=14, weight="bold"),
                                      text_color="#3b82f6")
        self.mem_label.pack(pady=(2, 8))

        # Threat Level
        threat_frame = ctk.CTkFrame(metrics_container, fg_color="transparent", corner_radius=16, height=80)
        threat_frame.pack(fill="x", pady=0)
        threat_frame.pack_propagate(False)

        ctk.CTkLabel(threat_frame, text="Threat Level", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(4, 4))
        self.threat_progress = ctk.CTkProgressBar(threat_frame, width=200, height=12, progress_color="#10b981")
        self.threat_progress.pack(pady=2)
        self.threat_label = ctk.CTkLabel(threat_frame, text="Low", font=ctk.CTkFont(size=14, weight="bold"),
                                         text_color="#10b981")
        self.threat_label.pack(pady=(2, 8))

    def create_network_health(self, parent):
        """Top-right panel - Network Health"""
        network_frame = ctk.CTkFrame(parent, fg_color="#132a3f", border_width=0, corner_radius=18)
        network_frame.grid(row=0, column=2, sticky="nsew", padx=(14, 14), pady=(14, 14))

        title = ctk.CTkLabel(network_frame, text="Network Health", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(8, 8))

        # Network metrics container
        net_container = ctk.CTkFrame(network_frame, fg_color="transparent")
        net_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Inbound Traffic
        inbound_frame = ctk.CTkFrame(net_container, fg_color="transparent", corner_radius=8, height=80)
        inbound_frame.pack(fill="x", pady=0)
        inbound_frame.pack_propagate(False)

        ctk.CTkLabel(inbound_frame, text="Inbound Traffic", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(0, 0))
        self.inbound_label = ctk.CTkLabel(inbound_frame, text="2.4 MB/s", font=ctk.CTkFont(size=14, weight="bold"),
                                          text_color="#10b981")
        self.inbound_label.pack(pady=(8, 8))

        # Outbound Traffic
        outbound_frame = ctk.CTkFrame(net_container, fg_color="transparent", corner_radius=8, height=80)
        outbound_frame.pack(fill="x", pady=0)
        outbound_frame.pack_propagate(False)

        ctk.CTkLabel(outbound_frame, text="Outbound Traffic", font=ctk.CTkFont(size=11, weight="bold")).pack(
            pady=(8, 4))
        self.outbound_label = ctk.CTkLabel(outbound_frame, text="1.8 MB/s", font=ctk.CTkFont(size=14, weight="bold"),
                                           text_color="#3b82f6")
        self.outbound_label.pack(pady=(8, 8))

        # Suspicious IPs
        suspicious_frame = ctk.CTkFrame(net_container, fg_color="transparent", corner_radius=8, height=80)
        suspicious_frame.pack(fill="x", pady=0)
        suspicious_frame.pack_propagate(False)

        ctk.CTkLabel(suspicious_frame, text="Suspicious IPs", font=ctk.CTkFont(size=11, weight="bold")).pack(
            pady=(8, 4))
        self.suspicious_label = ctk.CTkLabel(suspicious_frame, text="3 Blocked",
                                             font=ctk.CTkFont(size=14, weight="bold"), text_color="#ef4444")
        self.suspicious_label.pack(pady=(5, 5))

    def create_threats_panel(self, parent):
        """Bottom-left panel - Active Threats"""
        threats_frame = ctk.CTkFrame(parent, fg_color="#132a3f", border_width=0, corner_radius=18)
        threats_frame.grid(row=1, column=0, sticky="nsew", padx=(14, 14), pady=(14, 14))

        title = ctk.CTkLabel(threats_frame, text="Active Threats", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(15, 10))

        # Threats container with fixed height
        threats_container = ctk.CTkScrollableFrame(threats_frame, fg_color="#0f3460", height=280)
        threats_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        for threat in self.threats:
            threat_item = ctk.CTkFrame(threats_container, fg_color="#1e293b", corner_radius=6)
            threat_item.pack(fill="x", pady=3)

            # Threat info
            info_frame = ctk.CTkFrame(threat_item, fg_color="transparent")
            info_frame.pack(fill="x", padx=12, pady=8)

            name_label = ctk.CTkLabel(info_frame, text=threat["name"], font=ctk.CTkFont(size=11, weight="bold"),
                                      anchor="w")
            name_label.pack(fill="x")

            status_color = {"Quarantined": "#f59e0b", "Removed": "#10b981", "Detected": "#ef4444"}
            status_label = ctk.CTkLabel(info_frame, text=f"Status: {threat['status']}", font=ctk.CTkFont(size=10),
                                        text_color=status_color.get(threat["status"], "#94a3b8"), anchor="w")
            status_label.pack(fill="x")

            severity_label = ctk.CTkLabel(info_frame, text=f"Severity: {threat['severity']}", font=ctk.CTkFont(size=10),
                                          text_color="#64748b", anchor="w")
            severity_label.pack(fill="x")

    def create_scan_center(self, parent):
        """Center panel - Scan Controls"""
        # Create a circular/rounded center panel
        center_frame = ctk.CTkFrame(parent, fg_color="#14151b", border_width=0, border_color="#8b5cf6",corner_radius=25)
        center_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=20)

        # Configure center frame
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_rowconfigure(0, weight=0)
        center_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_rowconfigure(2, weight=0)
        center_frame.grid_rowconfigure(3, weight=0)

        # Title
        title = ctk.CTkLabel(center_frame, text="FIXION", font=ctk.CTkFont(size=38, weight="bold"))
        title.grid(row=0, column=0, pady=(20, 10))

        # Scan button container for circular button + label
        scan_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        scan_container.grid(row=1, column=0, pady=10)

        # Large circular scan button (empty text to keep it circular)
        self.scan_button = ctk.CTkButton(
            scan_container,
            text="",  # Empty text to maintain circular shape
            font=ctk.CTkFont(size=32, weight="bold"),
            width = 250,
            height=250,
            corner_radius=250,  # Make it circular
            fg_color="#047eaf",
            hover_color="#047eaf",
            command=self.start_scan
        )
        self.scan_button.pack()

        # Scan text label positioned over the button
        self.scan_text_label = ctk.CTkLabel(
            scan_container,
            text="SCAN",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white",
            fg_color="#047eaf"

        )
        # Position the label at the center of the button
        self.scan_text_label.place(in_=self.scan_button, relx=0.5, rely=0.5, anchor="center")

        # Progress section
        progress_frame = ctk.CTkFrame(center_frame, fg_color="#132a3f", corner_radius=15)
        progress_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=15, progress_color="#10b981", width=250)
        self.progress_bar.pack(pady=(15, 8))
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready to scan", font=ctk.CTkFont(size=12),
                                           text_color="#94a3b8")
        self.progress_label.pack(pady=(0, 10))

        # Scan options (compact)
        options_frame = ctk.CTkFrame(center_frame, fg_color="#132a3f", corner_radius=15)
        options_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(5, 15))

        self.scan_var = ctk.StringVar(value="Quick Scan")

        options_container = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_container.pack(anchor="center", padx=10, pady=10)

        quick_radio = ctk.CTkRadioButton(options_container, text="Quick", variable=self.scan_var, value="Quick Scan",
                                         font=ctk.CTkFont(size=11))
        quick_radio.pack(side="left", padx=(50,0))

        selective_radio = ctk.CTkRadioButton(options_container, text="Selective", variable=self.scan_var,
                                             value="Selective Scan", font=ctk.CTkFont(size=11))
        selective_radio.pack(side="left", padx=0)

        full_radio = ctk.CTkRadioButton(options_container, text="Full", variable=self.scan_var,
                                        value="Full System Scan", font=ctk.CTkFont(size=11))
        full_radio.pack(side="left", padx=0)

        # Stop button
        self.stop_button = ctk.CTkButton(
            options_frame,
            text="STOP",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=30,
            width=100,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.stop_scan,
            state="disabled"
        )
        self.stop_button.pack(pady=(0, 10))

    def create_rollback_panel(self, parent):
        """Bottom-right panel - System Rollback"""
        rollback_frame = ctk.CTkFrame(parent, fg_color="#132a3f", border_width=0, corner_radius=18)
        rollback_frame.grid(row=1, column=2, sticky="nsew", padx=(14, 14), pady=(14, 14))

        title = ctk.CTkLabel(rollback_frame, text="System Rollback", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(15, 10))

        # Rollback container
        rollback_container = ctk.CTkFrame(rollback_frame, fg_color="#0f3460", corner_radius=12)
        rollback_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Last backup info
        backup_info_frame = ctk.CTkFrame(rollback_container, fg_color="#1e293b", corner_radius=8)
        backup_info_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(backup_info_frame, text="Last Backup:", font=ctk.CTkFont(size=12, weight="bold")).pack(
            pady=(10, 2))
        ctk.CTkLabel(backup_info_frame, text="May 25, 2025 - 14:30", font=ctk.CTkFont(size=11),
                     text_color="#94a3b8").pack(pady=(0, 10))

        # Rollback buttons
        buttons_frame = ctk.CTkFrame(rollback_container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(10, 15))

        rollback_now_btn = ctk.CTkButton(
            buttons_frame,
            text="Rollback Now",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.rollback_now
        )
        rollback_now_btn.pack(fill="x", pady=3)

        schedule_btn = ctk.CTkButton(
            buttons_frame,
            text="Schedule Rollback",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=self.schedule_rollback
        )
        schedule_btn.pack(fill="x", pady=3)

        request_btn = ctk.CTkButton(
            buttons_frame,
            text="Request Rollback",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.request_rollback
        )
        request_btn.pack(fill="x", pady=3)

    def browse_selective_location(self):
        """Open file explorer to select scan location"""
        try:
            folder_path = filedialog.askdirectory(
                title="Select folder to scan",
                initialdir=os.path.expanduser("~")
            )
            if folder_path:
                self.selected_scan_path = folder_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file browser: {str(e)}")

    def start_scan(self):
        if not self.scanning:
            if self.scan_var.get() == "Selective Scan" and not self.selected_scan_path:
                self.browse_selective_location()
                if not self.selected_scan_path:
                    return

            self.scanning = True
            self.scan_type = self.scan_var.get()
            self.scan_button.configure(state="disabled")
            self.scan_text_label.configure(fg_color="#047eaf")
            self.scan_text_label.configure(text="SCANNING")
            self.stop_button.configure(state="normal")
            self.scan_threats_found = []

            # Start scan in separate thread
            scan_thread = threading.Thread(target=self.run_scan)
            scan_thread.daemon = True
            scan_thread.start()

    def run_scan(self):
        scan_files = {
            "Quick Scan": 1500,
            "Selective Scan": 500,
            "Full System Scan": 15000
        }

        self.total_files = scan_files.get(self.scan_type, 1500)
        self.files_scanned = 0

        while self.scanning and self.files_scanned < self.total_files:
            time.sleep(0.02)
            self.files_scanned += random.randint(1, 5)
            if self.files_scanned > self.total_files:
                self.files_scanned = self.total_files

            self.scan_progress = self.files_scanned / self.total_files
            self.root.after(0, self.update_scan_ui)

        if self.scanning:
            self.root.after(0, self.scan_complete)

    def update_scan_ui(self):
        self.progress_bar.set(self.scan_progress)
        progress_text = f"Scanning: {self.files_scanned:,}/{self.total_files:,} files ({int(self.scan_progress * 100)}%)"
        self.progress_label.configure(text=progress_text)

    def scan_complete(self):
        self.scanning = False
        self.scan_button.configure(state="normal")
        self.scan_text_label.configure(text="SCAN")
        self.scan_text_label.configure(fg_color="#047eaf")
        self.stop_button.configure(state="disabled")
        self.progress_label.configure(text=f"Scan Complete! {self.files_scanned:,} files scanned")
        self.show_scan_results()

    def stop_scan(self):
        self.scanning = False
        self.scan_button.configure(state="normal")
        self.scan_text_label.configure(text="SCAN")
        self.stop_button.configure(state="disabled")
        self.progress_label.configure(text="⏹ Scan stopped by user")

    def show_scan_results(self):
        """Show scan results in a popup dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Scan Results")
        dialog.geometry("400x300")
        dialog.configure(fg_color="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()

        title = ctk.CTkLabel(dialog, text="Scan Complete", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)

        summary_frame = ctk.CTkFrame(dialog, fg_color="#16213e")
        summary_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(summary_frame, text=f"Files Scanned: {self.files_scanned:,}", font=ctk.CTkFont(size=14)).pack(
            pady=5)
        ctk.CTkLabel(summary_frame, text=f"Threats Found: {len(self.scan_threats_found)}",
                     font=ctk.CTkFont(size=14)).pack(pady=5)

        if not self.scan_threats_found:
            ctk.CTkLabel(dialog, text="✅ No threats detected!", font=ctk.CTkFont(size=16, weight="bold"),
                         text_color="#10b981").pack(pady=20)

        ctk.CTkButton(dialog, text="Close", command=dialog.destroy, width=100, height=35).pack(pady=20)

    def update_system_metrics(self):
        cpu_usage = random.randint(30, 80)
        mem_usage = random.randint(45, 85)

        self.cpu_progress.set(cpu_usage / 100)
        self.cpu_label.configure(text=f"{cpu_usage}%")

        self.mem_progress.set(mem_usage / 100)
        self.mem_label.configure(text=f"{mem_usage}%")

        inbound = round(random.uniform(1.0, 5.0), 1)
        outbound = round(random.uniform(0.5, 3.0), 1)

        self.inbound_label.configure(text=f"{inbound} MB/s")
        self.outbound_label.configure(text=f"{outbound} MB/s")

        self.root.after(2000, self.update_system_metrics)

    def rollback_now(self):
        messagebox.showinfo("Rollback", "System rollback initiated!")

    def schedule_rollback(self):
        messagebox.showinfo("Schedule", "Rollback scheduling dialog would open here.")

    def request_rollback(self):
        messagebox.showinfo("Request", "Rollback request dialog would open here.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FixionDashboard()
    app.run()