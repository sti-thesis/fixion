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
from ai_scanner import AIAntivirusScanner

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FixionDashboard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Fixion Dashboard")

        # Make window responsive - minimum size but allow resizing
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.configure(fg_color="#1a1a2e")

        # Variables for scan functionality
        self.scanning = False
        self.scan_progress = 0
        self.current_file = ""
        self.files_scanned = 0
        self.total_files = 0
        self.scan_type = "Quick Scan"
        self.selected_scan_path = ""
        self.scan_threats_found = []
        self.scanner = AIAntivirusScanner()
        self.scanner.set_callbacks(
            file_scanned_callback=self.on_file_scanned,
            progress_callback=self.on_scan_progress,
            status_callback=self.on_status_update,
            result_callback=self.on_scan_result
        )

        # Sample data
        self.threats = [
            {"name": "Trojan.Generic.KD.123456", "status": "Quarantined", "severity": "High"},
            {"name": "Adware.BrowserModifier", "status": "Removed", "severity": "Medium"},
            {"name": "PUP.Optional.Download", "status": "Detected", "severity": "Low"}
        ]

        self.setup_ui()
        self.update_system_metrics()

    def setup_ui(self):
        # Create main scrollable frame
        self.main_scrollable = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent",
            scrollbar_button_color="#0f3460",
            scrollbar_button_hover_color="#16213e"
        )
        self.main_scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure grid weights for responsive behavior
        self.main_scrollable.grid_columnconfigure(0, weight=1)

        # Top section - Scan area
        self.create_scan_section(self.main_scrollable)

        # Middle section - System and Network Health
        self.create_health_section(self.main_scrollable)

        # Bottom section - Threats and Rollback
        self.create_bottom_section(self.main_scrollable)

    def create_scan_section(self, parent):
        # Responsive scan frame
        scan_frame = ctk.CTkFrame(parent, fg_color="#16213e", border_width=2, border_color="#0f3460")
        scan_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 10))
        scan_frame.grid_columnconfigure(0, weight=1)

        # Scan title
        title_label = ctk.CTkLabel(scan_frame, text="System Scan", font=ctk.CTkFont(size=20, weight="bold"),
                                   text_color="#ffffff")
        title_label.grid(row=0, column=0, pady=(15, 10), sticky="ew")

        # Main scan container - use grid for better responsiveness
        scan_container = ctk.CTkFrame(scan_frame, fg_color="transparent")
        scan_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        scan_container.grid_columnconfigure(0, weight=1)
        scan_container.grid_columnconfigure(1, weight=1)
        scan_container.grid_rowconfigure(0, weight=1)

        # Left side - Progress and file info (FIXED HEIGHT WITH SCROLLABLE CONTENT)
        left_frame = ctk.CTkFrame(scan_container, fg_color="#0f3460", corner_radius=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(3, weight=1)  # Make the files section expandable

        # Set a fixed height for the left frame to prevent expansion
        left_frame.configure(height=400)
        left_frame.grid_propagate(False)  # Prevent the frame from resizing based on content

        # Scan button (responsive size)
        self.scan_button = ctk.CTkButton(
            left_frame,
            text="SCAN",
            font=ctk.CTkFont(size=24, weight="bold"),
            height=60,
            corner_radius=30,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            command=self.start_scan
        )
        self.scan_button.grid(row=0, column=0, pady=(20, 15), padx=20, sticky="ew")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(left_frame, height=15, progress_color="#10b981")
        self.progress_bar.grid(row=1, column=0, pady=(0, 8), padx=20, sticky="ew")
        self.progress_bar.set(0)

        # Progress info
        self.progress_label = ctk.CTkLabel(left_frame, text="Ready to scan", font=ctk.CTkFont(size=12),
                                           text_color="#94a3b8")
        self.progress_label.grid(row=2, column=0, pady=(0, 8), padx=20, sticky="ew")

        # Files being scanned section (SCROLLABLE TO HANDLE OVERFLOW)
        files_frame = ctk.CTkScrollableFrame(left_frame, fg_color="#1e293b", corner_radius=10)
        files_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=(8, 15))

        files_title = ctk.CTkLabel(files_frame, text="Files Being Scanned:", font=ctk.CTkFont(size=11, weight="bold"),
                                   text_color="#ffffff")
        files_title.pack(pady=(8, 3), padx=8, anchor="w")

        # Current file being scanned
        self.file_label = ctk.CTkLabel(files_frame, text="Ready to scan...",
                                       font=ctk.CTkFont(size=10),
                                       text_color="#94a3b8",
                                       wraplength=250,
                                       justify="left",
                                       anchor="w")
        self.file_label.pack(pady=(0, 8), padx=8, anchor="w")

        # Right side - Manual scan options (ALSO FIXED HEIGHT)
        right_frame = ctk.CTkFrame(scan_container, fg_color="#0f3460", corner_radius=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)  # Make scan options expandable

        # Set matching fixed height and prevent propagation
        right_frame.configure(height=400)
        right_frame.grid_propagate(False)

        options_label = ctk.CTkLabel(right_frame, text="Scan Options", font=ctk.CTkFont(size=16, weight="bold"),
                                     text_color="#ffffff")
        options_label.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="ew")

        # Scan type selection in organized groups (SCROLLABLE CONTAINER)
        scan_options_frame = ctk.CTkScrollableFrame(right_frame, fg_color="#1e293b", corner_radius=10)
        scan_options_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))

        self.scan_var = ctk.StringVar(value="Quick Scan")

        # Quick Scan
        quick_frame = ctk.CTkFrame(scan_options_frame, fg_color="transparent")
        quick_frame.pack(fill="x", padx=10, pady=(8, 3))

        quick_radio = ctk.CTkRadioButton(quick_frame, text="Quick Scan", variable=self.scan_var, value="Quick Scan",
                                         font=ctk.CTkFont(size=12))
        quick_radio.pack(anchor="w")

        quick_desc = ctk.CTkLabel(quick_frame, text="Scans common threat locations (~5 minutes)",
                                  font=ctk.CTkFont(size=9), text_color="#64748b")
        quick_desc.pack(anchor="w", padx=15)

        # Selective Scan
        selective_frame = ctk.CTkFrame(scan_options_frame, fg_color="transparent")
        selective_frame.pack(fill="x", padx=10, pady=3)

        selective_radio = ctk.CTkRadioButton(selective_frame, text="Selective Scan", variable=self.scan_var,
                                             value="Selective Scan", font=ctk.CTkFont(size=12),
                                             command=self.on_scan_type_change)
        selective_radio.pack(anchor="w")

        selective_desc = ctk.CTkLabel(selective_frame, text="Scan specific folders or files",
                                      font=ctk.CTkFont(size=9), text_color="#64748b")
        selective_desc.pack(anchor="w", padx=15)

        # Browse button and path display for selective scan
        browse_frame = ctk.CTkFrame(selective_frame, fg_color="transparent")
        browse_frame.pack(fill="x", padx=15, pady=(3, 0))

        browse_container = ctk.CTkFrame(browse_frame, fg_color="transparent")
        browse_container.pack(fill="x")

        self.browse_button = ctk.CTkButton(
            browse_container,
            text="Browse",
            font=ctk.CTkFont(size=10),
            width=80,
            height=24,
            fg_color="#6366f1",
            hover_color="#4f46e5",
            command=self.browse_selective_location
        )
        self.browse_button.pack(side="left")

        self.selected_path_label = ctk.CTkLabel(browse_container, text="No location selected",
                                                font=ctk.CTkFont(size=9),
                                                text_color="#64748b",
                                                anchor="w")
        self.selected_path_label.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Full System Scan
        full_frame = ctk.CTkFrame(scan_options_frame, fg_color="transparent")
        full_frame.pack(fill="x", padx=10, pady=(3, 8))

        full_radio = ctk.CTkRadioButton(full_frame, text="Full System Scan", variable=self.scan_var,
                                        value="Full System Scan", font=ctk.CTkFont(size=12))
        full_radio.pack(anchor="w")

        full_desc = ctk.CTkLabel(full_frame, text="Complete system scan (~30-60 minutes)",
                                 font=ctk.CTkFont(size=9), text_color="#64748b")
        full_desc.pack(anchor="w", padx=15)

        # Stop button
        self.stop_button = ctk.CTkButton(
            right_frame,
            text="STOP SCAN",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.stop_scan,
            state="disabled"
        )
        self.stop_button.grid(row=2, column=0, pady=(10, 15), padx=15, sticky="ew")

    def on_file_scanned(self, file_path, result):
        self.root.after(0, lambda: self._update_file_scanned(file_path, result))

    def _update_file_scanned(self, file_path, result):
        self.scan_threats_found.append(result)
        self.update_scan_ui()

    def on_scan_progress(self, current, total, current_file):
        self.root.after(0, lambda: self._update_progress(current, total, current_file))

    def _update_progress(self, current, total, current_file):
        self.files_scanned = current
        self.total_files = total
        self.current_file = current_file
        self.scan_progress = current / total if total else 0
        self.update_scan_ui()

    def on_status_update(self, message):
        print(f"Scanner Status: {message}")  # Optional: Display in UI or console

    def on_scan_result(self, result):
        # You can extend this to display popups for threats
        pass

    def browse_selective_location(self):
        """Open file explorer to select scan location"""
        try:
            folder_path = filedialog.askdirectory(
                title="Select folder to scan",
                initialdir=os.path.expanduser("~")
            )

            if folder_path:
                self.selected_scan_path = folder_path
                if len(folder_path) > 25:
                    display_path = "..." + folder_path[-22:]
                else:
                    display_path = folder_path
                self.selected_path_label.configure(text=display_path, text_color="#10b981")
            else:
                self.selected_scan_path = ""
                self.selected_path_label.configure(text="No location selected", text_color="#64748b")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file browser: {str(e)}")

    def on_scan_type_change(self):
        """Handle scan type changes"""
        if self.scan_var.get() == "Selective Scan":
            self.browse_button.configure(state="normal")
        else:
            self.browse_button.configure(state="disabled")

    def create_health_section(self, parent):
        health_container = ctk.CTkFrame(parent, fg_color="transparent")
        health_container.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))
        health_container.grid_columnconfigure(0, weight=1)
        health_container.grid_columnconfigure(1, weight=1)

        # System Health
        system_frame = ctk.CTkFrame(health_container, fg_color="#16213e", border_width=2, border_color="#0f3460")
        system_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        system_frame.grid_columnconfigure(0, weight=1)

        system_title = ctk.CTkLabel(system_frame, text="System Health", font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color="#ffffff")
        system_title.grid(row=0, column=0, pady=(12, 8))

        # System metrics container
        metrics_container = ctk.CTkFrame(system_frame, fg_color="transparent")
        metrics_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        metrics_container.grid_columnconfigure(0, weight=1)
        metrics_container.grid_columnconfigure(1, weight=1)
        metrics_container.grid_columnconfigure(2, weight=1)

        # CPU Usage
        cpu_frame = ctk.CTkFrame(metrics_container, fg_color="#0f3460", corner_radius=8)
        cpu_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 2))

        ctk.CTkLabel(cpu_frame, text="CPU Usage", font=ctk.CTkFont(size=10, weight="bold")).pack(pady=(8, 4))
        self.cpu_progress = ctk.CTkProgressBar(cpu_frame, width=80, height=12, progress_color="#f59e0b")
        self.cpu_progress.pack(pady=(0, 4))
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="45%", font=ctk.CTkFont(size=12, weight="bold"),
                                      text_color="#f59e0b")
        self.cpu_label.pack(pady=(0, 8))

        # Memory Usage
        mem_frame = ctk.CTkFrame(metrics_container, fg_color="#0f3460", corner_radius=8)
        mem_frame.grid(row=0, column=1, sticky="nsew", padx=2)

        ctk.CTkLabel(mem_frame, text="Memory Usage", font=ctk.CTkFont(size=10, weight="bold")).pack(pady=(8, 4))
        self.mem_progress = ctk.CTkProgressBar(mem_frame, width=80, height=12, progress_color="#3b82f6")
        self.mem_progress.pack(pady=(0, 4))
        self.mem_label = ctk.CTkLabel(mem_frame, text="68%", font=ctk.CTkFont(size=12, weight="bold"),
                                      text_color="#3b82f6")
        self.mem_label.pack(pady=(0, 8))

        # Threat Level
        threat_frame = ctk.CTkFrame(metrics_container, fg_color="#0f3460", corner_radius=8)
        threat_frame.grid(row=0, column=2, sticky="nsew", padx=(2, 0))

        ctk.CTkLabel(threat_frame, text="Threat Level", font=ctk.CTkFont(size=10, weight="bold")).pack(pady=(8, 4))
        self.threat_progress = ctk.CTkProgressBar(threat_frame, width=80, height=12, progress_color="#10b981")
        self.threat_progress.pack(pady=(0, 4))
        self.threat_label = ctk.CTkLabel(threat_frame, text="Low", font=ctk.CTkFont(size=12, weight="bold"),
                                         text_color="#10b981")
        self.threat_label.pack(pady=(0, 8))

        # Network Health
        network_frame = ctk.CTkFrame(health_container, fg_color="#16213e", border_width=2, border_color="#0f3460")
        network_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        network_frame.grid_columnconfigure(0, weight=1)

        network_title = ctk.CTkLabel(network_frame, text="Network Health", font=ctk.CTkFont(size=16, weight="bold"),
                                     text_color="#ffffff")
        network_title.grid(row=0, column=0, pady=(12, 8))

        # Network metrics
        net_metrics_container = ctk.CTkFrame(network_frame, fg_color="transparent")
        net_metrics_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        net_metrics_container.grid_columnconfigure(0, weight=1)
        net_metrics_container.grid_columnconfigure(1, weight=1)
        net_metrics_container.grid_columnconfigure(2, weight=1)

        # Inbound
        inbound_frame = ctk.CTkFrame(net_metrics_container, fg_color="#0f3460", corner_radius=8)
        inbound_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 2))

        ctk.CTkLabel(inbound_frame, text="Inbound", font=ctk.CTkFont(size=10, weight="bold")).pack(pady=(8, 4))
        self.inbound_label = ctk.CTkLabel(inbound_frame, text="2.4 MB/s", font=ctk.CTkFont(size=11, weight="bold"),
                                          text_color="#10b981")
        self.inbound_label.pack(pady=(0, 8))

        # Outbound
        outbound_frame = ctk.CTkFrame(net_metrics_container, fg_color="#0f3460", corner_radius=8)
        outbound_frame.grid(row=0, column=1, sticky="nsew", padx=2)

        ctk.CTkLabel(outbound_frame, text="Outbound", font=ctk.CTkFont(size=10, weight="bold")).pack(pady=(8, 4))
        self.outbound_label = ctk.CTkLabel(outbound_frame, text="1.8 MB/s", font=ctk.CTkFont(size=11, weight="bold"),
                                           text_color="#3b82f6")
        self.outbound_label.pack(pady=(0, 8))

        # Suspicious IPs
        suspicious_frame = ctk.CTkFrame(net_metrics_container, fg_color="#0f3460", corner_radius=8)
        suspicious_frame.grid(row=0, column=2, sticky="nsew", padx=(2, 0))

        ctk.CTkLabel(suspicious_frame, text="Suspicious IP's", font=ctk.CTkFont(size=10, weight="bold")).pack(
            pady=(8, 4))
        self.suspicious_label = ctk.CTkLabel(suspicious_frame, text="3 Blocked",
                                             font=ctk.CTkFont(size=11, weight="bold"), text_color="#ef4444")
        self.suspicious_label.pack(pady=(0, 8))

    def create_bottom_section(self, parent):
        bottom_container = ctk.CTkFrame(parent, fg_color="transparent")
        bottom_container.grid(row=2, column=0, sticky="ew", padx=5)
        bottom_container.grid_columnconfigure(0, weight=1)
        bottom_container.grid_columnconfigure(1, weight=1)

        # Active Threats
        threats_frame = ctk.CTkFrame(bottom_container, fg_color="#16213e", border_width=2, border_color="#0f3460")
        threats_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        threats_frame.grid_columnconfigure(0, weight=1)
        threats_frame.grid_rowconfigure(1, weight=1)

        threats_title = ctk.CTkLabel(threats_frame, text="Active Threats", font=ctk.CTkFont(size=16, weight="bold"),
                                     text_color="#ffffff")
        threats_title.grid(row=0, column=0, pady=(12, 8))

        # Threats list with scrollable frame
        threats_container = ctk.CTkScrollableFrame(threats_frame, fg_color="#0f3460", height=200)
        threats_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

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
            status_label = ctk.CTkLabel(info_frame, text=f"Status: {threat['status']}",
                                        font=ctk.CTkFont(size=10),
                                        text_color=status_color.get(threat["status"], "#94a3b8"),
                                        anchor="w")
            status_label.pack(fill="x")

            severity_label = ctk.CTkLabel(info_frame, text=f"Severity: {threat['severity']}",
                                          font=ctk.CTkFont(size=10),
                                          text_color="#64748b",
                                          anchor="w")
            severity_label.pack(fill="x")

        # Request Rollback
        rollback_frame = ctk.CTkFrame(bottom_container, fg_color="#16213e", border_width=2, border_color="#0f3460")
        rollback_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        rollback_frame.grid_columnconfigure(0, weight=1)

        rollback_title = ctk.CTkLabel(rollback_frame, text="System Rollback", font=ctk.CTkFont(size=16, weight="bold"),
                                      text_color="#ffffff")
        rollback_title.grid(row=0, column=0, pady=(12, 8))

        # Rollback options
        rollback_container = ctk.CTkFrame(rollback_frame, fg_color="#0f3460", corner_radius=12)
        rollback_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        rollback_container.grid_columnconfigure(0, weight=1)

        # Last backup info
        backup_info = ctk.CTkLabel(rollback_container, text="Last Backup:", font=ctk.CTkFont(size=11, weight="bold"))
        backup_info.grid(row=0, column=0, pady=(15, 3))

        backup_date = ctk.CTkLabel(rollback_container, text="May 25, 2025 - 14:30", font=ctk.CTkFont(size=10),
                                   text_color="#94a3b8")
        backup_date.grid(row=1, column=0, pady=(0, 12))

        # Rollback buttons
        rollback_now_btn = ctk.CTkButton(
            rollback_container,
            text="Rollback Now",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=32,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.rollback_now
        )
        rollback_now_btn.grid(row=2, column=0, pady=3, padx=20, sticky="ew")

        schedule_btn = ctk.CTkButton(
            rollback_container,
            text="Schedule Rollback",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=32,
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=self.schedule_rollback
        )
        schedule_btn.grid(row=3, column=0, pady=3, padx=20, sticky="ew")

        request_btn = ctk.CTkButton(
            rollback_container,
            text="Request Rollback",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=32,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.request_rollback
        )
        request_btn.grid(row=4, column=0, pady=(3, 15), padx=20, sticky="ew")

    def start_scan(self):
        if not self.scanning:
            if self.scan_var.get() == "Selective Scan" and not self.selected_scan_path:
                self.show_error_dialog("Please select a location to scan for Selective Scan.")
                return

            self.scanning = True
            self.scan_type = self.scan_var.get()
            self.scan_button.configure(state="disabled", text="SCANNING...")
            self.stop_button.configure(state="normal")
            self.scan_threats_found = []

            # Start scan in a new thread
            threading.Thread(target=self.run_real_scan, daemon=True).start()

    def run_real_scan(self):
        def scanning_task():
            if self.scan_type == "Quick Scan":
                results = self.scanner.quick_scan()
            elif self.scan_type == "Full System Scan":
                results = self.scanner.full_scan()
            elif self.scan_type == "Selective Scan":
                results = self.scanner.selective_scan([self.selected_scan_path])
            else:
                results = []

            # When scan completes, update UI in main thread
            self.root.after(0, self.scan_complete)

        # Start the scanning task in a separate thread
        threading.Thread(target=scanning_task, daemon=True).start()

    def update_scan_ui(self):
        self.progress_bar.set(self.scan_progress)
        progress_text = f"Scanning: {self.files_scanned:,}/{self.total_files:,} files ({int(self.scan_progress * 100)}%)"
        self.progress_label.configure(text=progress_text)

        # Format file path for better readability
        if self.current_file:
            formatted_file = self.current_file.replace("\\", " → ")
            if len(formatted_file) > 50:
                formatted_file = "..." + formatted_file[-47:]
            self.file_label.configure(text=formatted_file)
        else:
            self.file_label.configure(text="Ready to scan...")

    def scan_complete(self):
        self.scanning = False
        self.scan_button.configure(state="normal", text="SCAN")
        self.stop_button.configure(state="disabled")
        self.progress_label.configure(text=f"Scan Complete! {self.files_scanned:,} files scanned")

        # Show scan results popup
        self.show_scan_results()

    def stop_scan(self):
        self.scanner.stop_scan()
        self.scanning = False
        self.scan_button.configure(state="normal", text="SCAN")
        self.stop_button.configure(state="disabled")
        self.progress_label.configure(text="⏹ Scan stopped by user")
        self.file_label.configure(text="Ready to scan...")

    def show_scan_results(self):
        """Show scan results in a popup dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Scan Results")
        dialog.geometry("500x400")
        dialog.configure(fg_color="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 100))

        title = ctk.CTkLabel(dialog, text="Scan Complete", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)

        # Results summary
        summary_frame = ctk.CTkFrame(dialog, fg_color="#16213e")
        summary_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(summary_frame, text=f"Files Scanned: {self.files_scanned:,}",
                     font=ctk.CTkFont(size=14)).pack(pady=5)
        ctk.CTkLabel(summary_frame, text=f"Threats Found: {len(self.scan_threats_found)}",
                     font=ctk.CTkFont(size=14)).pack(pady=5)

        # Threats found
        if self.scan_threats_found:
            threats_label = ctk.CTkLabel(dialog, text="Threats Detected:",
                                         font=ctk.CTkFont(size=14, weight="bold"), text_color="#ef4444")
            threats_label.pack(pady=(10, 5))

            threats_frame = ctk.CTkScrollableFrame(dialog, height=150, fg_color="#16213e")
            threats_frame.pack(fill="both", expand=True, padx=20, pady=10)

            for threat in self.scan_threats_found:
                threat_item = ctk.CTkFrame(threats_frame, fg_color="#0f3460")
                threat_item.pack(fill="x", pady=2)

                ctk.CTkLabel(threat_item, text=threat["name"], font=ctk.CTkFont(size=12, weight="bold"),
                             anchor="w").pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(threat_item, text=f"Severity: {threat['severity']}",
                             font=ctk.CTkFont(size=10), text_color="#94a3b8",
                             anchor="w").pack(fill="x", padx=10, pady=(0, 5))
        else:
            ctk.CTkLabel(dialog, text="✅ No threats detected!",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#10b981").pack(pady=20)

        # Close button
        ctk.CTkButton(dialog, text="Close", command=dialog.destroy,
                      width=100, height=35).pack(pady=20)

    def show_error_dialog(self, message):
        """Show error dialog"""
        messagebox.showerror("Error", message)

    def update_system_metrics(self):
        # Simulate dynamic system metrics
        cpu_usage = random.randint(30, 80)
        mem_usage = random.randint(45, 85)

        self.cpu_progress.set(cpu_usage / 100)
        self.cpu_label.configure(text=f"{cpu_usage}%")

        self.mem_progress.set(mem_usage / 100)
        self.mem_label.configure(text=f"{mem_usage}%")

        # Update network metrics
        inbound = round(random.uniform(1.0, 5.0), 1)
        outbound = round(random.uniform(0.5, 3.0), 1)

        self.inbound_label.configure(text=f"{inbound} MB/s")
        self.outbound_label.configure(text=f"{outbound} MB/s")

        # Schedule next update
        self.root.after(2000, self.update_system_metrics)

    def rollback_now(self):
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Confirm Rollback")
        dialog.geometry("400x200")
        dialog.configure(fg_color="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text="Are you sure you want to rollback now?\nThis will restart your system.",
                             font=ctk.CTkFont(size=14), text_color="#ffffff")
        label.pack(pady=30)

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)

        confirm_btn = ctk.CTkButton(button_frame, text="Confirm", fg_color="#ef4444", hover_color="#dc2626",
                                    command=lambda: [dialog.destroy(), self.execute_rollback()])
        confirm_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", fg_color="#64748b", hover_color="#475569",
                                   command=dialog.destroy)
        cancel_btn.pack(side="right", padx=10)

    def schedule_rollback(self):
        # Create schedule dialog with proper Windows-style calendar
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Schedule Rollback")
        dialog.geometry("700x750")
        dialog.configure(fg_color="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))

        title_label = ctk.CTkLabel(dialog, text="Schedule System Rollback", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=20)

        # Main container
        main_container = ctk.CTkFrame(dialog, fg_color="#16213e")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Calendar section
        calendar_section = ctk.CTkFrame(main_container, fg_color="#0f3460")
        calendar_section.pack(fill="both", expand=True, padx=20, pady=20)

        cal_title = ctk.CTkLabel(calendar_section, text="Select Date:", font=ctk.CTkFont(size=16, weight="bold"))
        cal_title.pack(pady=(15, 10))

        # Calendar widget
        self.create_calendar_widget(calendar_section, dialog)

        # Time selection
        time_frame = ctk.CTkFrame(main_container, fg_color="#0f3460")
        time_frame.pack(fill="x", padx=20, pady=(0, 20))

        time_title = ctk.CTkLabel(time_frame, text="Select Time:", font=ctk.CTkFont(size=16, weight="bold"))
        time_title.pack(pady=(15, 10))

        time_container = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_container.pack(pady=10)

        # Hour selection
        hour_frame = ctk.CTkFrame(time_container, fg_color="transparent")
        hour_frame.pack(side="left", padx=10)

        ctk.CTkLabel(hour_frame, text="Hour:", font=ctk.CTkFont(size=12)).pack()
        self.hour_var = ctk.StringVar(value="12")
        hour_menu = ctk.CTkOptionMenu(hour_frame, variable=self.hour_var,
                                      values=[f"{i:02d}" for i in range(1, 13)])
        hour_menu.pack(pady=5)

        # Minute selection
        minute_frame = ctk.CTkFrame(time_container, fg_color="transparent")
        minute_frame.pack(side="left", padx=10)

        ctk.CTkLabel(minute_frame, text="Minute:", font=ctk.CTkFont(size=12)).pack()
        self.minute_var = ctk.StringVar(value="00")
        minute_menu = ctk.CTkOptionMenu(minute_frame, variable=self.minute_var,
                                        values=[f"{i:02d}" for i in range(0, 60, 15)])
        minute_menu.pack(pady=5)

        # AM/PM selection
        ampm_frame = ctk.CTkFrame(time_container, fg_color="transparent")
        ampm_frame.pack(side="left", padx=10)

        ctk.CTkLabel(ampm_frame, text="AM/PM:", font=ctk.CTkFont(size=12)).pack()
        self.ampm_var = ctk.StringVar(value="PM")
        ampm_menu = ctk.CTkOptionMenu(ampm_frame, variable=self.ampm_var, values=["AM", "PM"])
        ampm_menu.pack(pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        button_frame.pack(pady=20)

        schedule_btn = ctk.CTkButton(button_frame, text="Schedule Rollback",
                                     fg_color="#10b981", hover_color="#059669",
                                     command=lambda: self.confirm_schedule(dialog))
        schedule_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel",
                                   fg_color="#64748b", hover_color="#475569",
                                   command=dialog.destroy)
        cancel_btn.pack(side="right", padx=10)

    def create_calendar_widget(self, parent, dialog):
        """Create a Windows-style calendar widget"""
        # Initialize calendar variables
        self.current_date = datetime.now()
        self.selected_date = self.current_date

        # Calendar navigation frame
        nav_frame = ctk.CTkFrame(parent, fg_color="#1e293b")
        nav_frame.pack(fill="x", padx=20, pady=10)

        # Previous button
        prev_btn = ctk.CTkButton(nav_frame, text="◀", width=40, height=30,
                                 command=self.prev_month, fg_color="#3b82f6")
        prev_btn.pack(side="left", padx=5, pady=5)

        # Month/Year display
        self.month_year_label = ctk.CTkLabel(nav_frame, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.month_year_label.pack(side="left", expand=True, padx=20, pady=5)

        # Next button
        next_btn = ctk.CTkButton(nav_frame, text="▶", width=40, height=30,
                                 command=self.next_month, fg_color="#3b82f6")
        next_btn.pack(side="right", padx=5, pady=5)

        # Calendar grid frame
        self.calendar_frame = ctk.CTkFrame(parent, fg_color="#1e293b")
        self.calendar_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Day headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days):
            day_label = ctk.CTkLabel(self.calendar_frame, text=day, font=ctk.CTkFont(size=12, weight="bold"),
                                     text_color="#94a3b8")
            day_label.grid(row=0, column=i, padx=2, pady=5, sticky="nsew")

        # Configure grid weights
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):  # 6 weeks + header
            self.calendar_frame.grid_rowconfigure(i, weight=1)

        self.update_calendar()

    def prev_month(self):
        """Go to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()

    def next_month(self):
        """Go to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()

    def update_calendar(self):
        """Update the calendar display"""
        # Update month/year label
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        self.month_year_label.configure(text=f"{month_names[self.current_date.month - 1]} {self.current_date.year}")

        # Clear existing day buttons
        for widget in self.calendar_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:  # Don't remove day headers
                widget.destroy()

        # Get calendar data
        cal = cal_module.monthcalendar(self.current_date.year, self.current_date.month)

        # Create day buttons
        today = datetime.now().date()
        selected_date = self.selected_date.date() if hasattr(self.selected_date, 'date') else self.selected_date

        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell for days from other months
                    continue

                date_obj = datetime(self.current_date.year, self.current_date.month, day).date()

                # Determine button color
                if date_obj == today:
                    # Today
                    btn_color = "#f59e0b"
                    hover_color = "#d97706"
                elif date_obj == selected_date:
                    # Selected date
                    btn_color = "#10b981"
                    hover_color = "#059669"
                elif date_obj < today:
                    # Past dates (disabled)
                    btn_color = "#374151"
                    hover_color = "#374151"
                else:
                    # Future dates
                    btn_color = "#4b5563"
                    hover_color = "#6b7280"

                day_btn = ctk.CTkButton(
                    self.calendar_frame,
                    text=str(day),
                    width=40,
                    height=40,
                    font=ctk.CTkFont(size=12),
                    fg_color=btn_color,
                    hover_color=hover_color,
                    command=lambda d=day: self.select_date(d)
                )

                # Disable past dates
                if date_obj < today:
                    day_btn.configure(state="disabled")

                day_btn.grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")

    def select_date(self, day):
        """Select a date on the calendar"""
        self.selected_date = datetime(self.current_date.year, self.current_date.month, day)
        self.update_calendar()

    def confirm_schedule(self, dialog):
        """Confirm the scheduled rollback"""
        # Format the scheduled date and time
        selected_datetime = self.selected_date.replace(
            hour=int(self.hour_var.get()) + (12 if self.ampm_var.get() == "PM" and self.hour_var.get() != "12" else 0),
            minute=int(self.minute_var.get())
        )

        if self.ampm_var.get() == "AM" and self.hour_var.get() == "12":
            selected_datetime = selected_datetime.replace(hour=0)

        # Check if the selected time is in the future
        if selected_datetime <= datetime.now():
            messagebox.showerror("Invalid Time", "Please select a future date and time.")
            return

        formatted_datetime = selected_datetime.strftime("%B %d, %Y at %I:%M %p")

        # Show confirmation
        confirm_dialog = ctk.CTkToplevel(dialog)
        confirm_dialog.title("Confirm Schedule")
        confirm_dialog.geometry("450x250")
        confirm_dialog.configure(fg_color="#1a1a2e")
        confirm_dialog.transient(dialog)
        confirm_dialog.grab_set()

        # Center the confirmation dialog
        confirm_dialog.geometry("+%d+%d" % (dialog.winfo_rootx() + 100, dialog.winfo_rooty() + 200))

        ctk.CTkLabel(confirm_dialog, text="Rollback Scheduled",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        ctk.CTkLabel(confirm_dialog, text=f"System rollback has been scheduled for:\n{formatted_datetime}",
                     font=ctk.CTkFont(size=14), text_color="#94a3b8").pack(pady=20)

        ctk.CTkLabel(confirm_dialog, text="You will receive a notification before the rollback begins.",
                     font=ctk.CTkFont(size=12), text_color="#64748b").pack(pady=10)

        btn_frame = ctk.CTkFrame(confirm_dialog, fg_color="transparent")
        btn_frame.pack(pady=30)

        ctk.CTkButton(btn_frame, text="OK", width=100,
                      command=lambda: [confirm_dialog.destroy(), dialog.destroy()]).pack()

    def request_rollback(self):
        # Create request dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Request Rollback")
        dialog.geometry("500x400")
        dialog.configure(fg_color="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()

        title = ctk.CTkLabel(dialog, text="Request System Rollback", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)

        # Request form
        form_frame = ctk.CTkFrame(dialog, fg_color="#16213e")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Reason selection
        reason_label = ctk.CTkLabel(form_frame, text="Reason for rollback:", font=ctk.CTkFont(size=14, weight="bold"))
        reason_label.pack(pady=(20, 10))

        self.reason_var = ctk.StringVar(value="System Performance Issues")
        reasons = [
            "System Performance Issues",
            "Software Compatibility Problems",
            "Security Concerns",
            "System Instability",
            "Other (specify below)"
        ]

        for reason in reasons:
            radio = ctk.CTkRadioButton(form_frame, text=reason, variable=self.reason_var, value=reason)
            radio.pack(anchor="w", padx=20, pady=2)

        # Additional details
        details_label = ctk.CTkLabel(form_frame, text="Additional details:", font=ctk.CTkFont(size=14, weight="bold"))
        details_label.pack(pady=(20, 10))

        self.details_text = ctk.CTkTextbox(form_frame, height=100, width=400)
        self.details_text.pack(padx=20, pady=10)
        self.details_text.insert("1.0", "Please describe the issues you're experiencing...")

        # Priority selection
        priority_label = ctk.CTkLabel(form_frame, text="Priority:", font=ctk.CTkFont(size=14, weight="bold"))
        priority_label.pack(pady=(10, 5))

        self.priority_var = ctk.StringVar(value="Normal")
        priority_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        priority_frame.pack(pady=5)

        priorities = ["Low", "Normal", "High", "Critical"]
        for priority in priorities:
            radio = ctk.CTkRadioButton(priority_frame, text=priority, variable=self.priority_var, value=priority)
            radio.pack(side="left", padx=10)

        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        submit_btn = ctk.CTkButton(button_frame, text="Submit Request",
                                   fg_color="#10b981", hover_color="#059669",
                                   command=lambda: self.submit_rollback_request(dialog))
        submit_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel",
                                   fg_color="#64748b", hover_color="#475569",
                                   command=dialog.destroy)
        cancel_btn.pack(side="right", padx=10)

    def submit_rollback_request(self, dialog):
        """Submit the rollback request"""
        # Get request details
        reason = self.reason_var.get()
        details = self.details_text.get("1.0", "end-1c")
        priority = self.priority_var.get()

        # Show confirmation
        success_dialog = ctk.CTkToplevel(dialog)
        success_dialog.title("Request Submitted")
        success_dialog.geometry("400x300")
        success_dialog.configure(fg_color="#1a1a2e")
        success_dialog.transient(dialog)
        success_dialog.grab_set()

        # Center the dialog
        success_dialog.geometry("+%d+%d" % (dialog.winfo_rootx() + 50, dialog.winfo_rooty() + 50))

        ctk.CTkLabel(success_dialog, text="✅ Request Submitted",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#10b981").pack(pady=20)

        # Request ID
        request_id = f"RB-{random.randint(10000, 99999)}"
        ctk.CTkLabel(success_dialog, text=f"Request ID: {request_id}",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)

        # Summary
        summary_frame = ctk.CTkFrame(success_dialog, fg_color="#16213e")
        summary_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(summary_frame, text=f"Reason: {reason}",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkLabel(summary_frame, text=f"Priority: {priority}",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=2)

        ctk.CTkLabel(success_dialog,
                     text="Your request has been submitted to the IT department.\nYou will be notified of the approval status.",
                     font=ctk.CTkFont(size=12), text_color="#94a3b8").pack(pady=20)

        ctk.CTkButton(success_dialog, text="Close", width=100,
                      command=lambda: [success_dialog.destroy(), dialog.destroy()]).pack(pady=10)

    def execute_rollback(self):
        """Execute immediate rollback"""
        # Show rollback progress
        progress_dialog = ctk.CTkToplevel(self.root)
        progress_dialog.title("System Rollback")
        progress_dialog.geometry("400x200")
        progress_dialog.configure(fg_color="#1a1a2e")
        progress_dialog.transient(self.root)
        progress_dialog.grab_set()

        ctk.CTkLabel(progress_dialog, text="Initiating System Rollback...",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=30)

        progress_bar = ctk.CTkProgressBar(progress_dialog, width=300)
        progress_bar.pack(pady=20)
        progress_bar.set(0)

        status_label = ctk.CTkLabel(progress_dialog, text="Preparing rollback...",
                                    font=ctk.CTkFont(size=12), text_color="#94a3b8")
        status_label.pack(pady=10)

        # Simulate rollback progress
        def update_progress():
            for i in range(101):
                progress_bar.set(i / 100)
                if i < 20:
                    status_label.configure(text="Stopping services...")
                elif i < 40:
                    status_label.configure(text="Creating backup...")
                elif i < 60:
                    status_label.configure(text="Restoring system files...")
                elif i < 80:
                    status_label.configure(text="Updating registry...")
                else:
                    status_label.configure(text="Finalizing rollback...")

                progress_dialog.update()
                time.sleep(0.05)

            status_label.configure(text="Rollback complete! System will restart in 10 seconds...")
            progress_dialog.after(3000, progress_dialog.destroy)

        # Start progress in thread
        threading.Thread(target=update_progress, daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FixionDashboard()
    app.run()