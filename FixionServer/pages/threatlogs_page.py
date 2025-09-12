import customtkinter
import tkinter as tk
from tkinter import ttk
import datetime
from PIL import Image
import os

# Sample threat data - in a real app, this would come from a database
sample_threats = [
    {
        "id": "TH001",
        "timestamp": "2025-04-08 14:23:15",
        "type": "Malware",
        "severity": "High",
        "client_machine": "DESKTOP-AB123",
        "description": "Trojan detected in system files",
        "affected_files": ["C:\\Windows\\System32\\svchost.exe",
                           "C:\\Users\\Admin\\AppData\\Local\\Temp\\suspicious.dll"],
        "machine_info": {
            "os": "Windows 11 Pro",
            "ip": "192.168.1.105",
            "location": "Marketing Department"
        },
        "action_taken": "Quarantined"
    },
    {
        "id": "TH002",
        "timestamp": "2025-04-09 08:45:32",
        "type": "Unauthorized Access",
        "severity": "Critical",
        "client_machine": "SERVER-DB01",
        "description": "Multiple failed login attempts detected",
        "affected_files": [],
        "machine_info": {
            "os": "Windows Server 2022",
            "ip": "192.168.1.5",
            "location": "Server Room"
        },
        "action_taken": "IP blocked"
    },
    {
        "id": "TH003",
        "timestamp": "2025-04-09 10:12:45",
        "type": "Phishing",
        "severity": "Medium",
        "client_machine": "LAPTOP-XYZ789",
        "description": "Suspicious email link clicked",
        "affected_files": ["C:\\Users\\JDoe\\Downloads\\invoice.pdf.exe"],
        "machine_info": {
            "os": "Windows 10 Enterprise",
            "ip": "192.168.1.78",
            "location": "Sales Department"
        },
        "action_taken": "File deleted, user notified"
    },
    {
        "id": "TH004",
        "timestamp": "2025-04-10 02:34:11",
        "type": "Ransomware",
        "severity": "Critical",
        "client_machine": "DESKTOP-QR456",
        "description": "Encryption activity detected on multiple files",
        "affected_files": ["D:\\Shared\\financial_reports\\*.xlsx", "D:\\Shared\\customer_data\\*.csv"],
        "machine_info": {
            "os": "Windows 10 Pro",
            "ip": "192.168.1.42",
            "location": "Finance Department"
        },
        "action_taken": "System isolated, restore from backup initiated"
    },
    {
        "id": "TH005",
        "timestamp": "2025-04-10 09:17:22",
        "type": "Data Exfiltration",
        "severity": "High",
        "client_machine": "LAPTOP-JK321",
        "description": "Unusual outbound data transfer detected",
        "affected_files": ["C:\\Users\\MSmith\\Documents\\company_strategy.docx"],
        "machine_info": {
            "os": "Windows 11 Enterprise",
            "ip": "192.168.1.156",
            "location": "Executive Office"
        },
        "action_taken": "Connection terminated, investigation ongoing"
    }
]

# Get current directory for assets
current_dir = os.path.dirname(os.path.abspath(__file__))


def get_assets_path():
    """Find the assets directory regardless of where the script is run from"""
    # Try direct path
    direct_path = os.path.join(current_dir, "assets")
    if os.path.exists(direct_path):
        return direct_path

    # Try going up one directory
    parent_path = os.path.join(current_dir, "..", "assets")
    if os.path.exists(parent_path):
        return parent_path

    return "assets"  # Fallback to relative path


# Use this function to get assets path
assets_path = get_assets_path()


class ScrollableTreeView(customtkinter.CTkFrame):
    """Custom scrollable treeview widget"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a frame for the treeview and scrollbar
        self.tree_frame = customtkinter.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True)

        # Create a Treeview widget
        self.tree = ttk.Treeview(self.tree_frame)

        # Create scrollbars
        self.vsb = customtkinter.CTkScrollbar(self.tree_frame, command=self.tree.yview)
        self.hsb = customtkinter.CTkScrollbar(self.tree_frame, orientation="horizontal", command=self.tree.xview)

        # Configure the treeview to use scrollbars
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Pack scrollbars and treeview
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Create custom style for the treeview
        style = ttk.Style()
        style.theme_use("default")

        # Configure the Treeview colors
        style.configure("Treeview",
                        background="#1c253a",
                        foreground="#ffffff",
                        fieldbackground="#1c253a",
                        borderwidth=0)

        style.map('Treeview',
                  background=[('selected', '#4e288b')],
                  foreground=[('selected', '#ffffff')])

        # Configure the header appearance
        style.configure("Treeview.Heading",
                        background="#283146",
                        foreground="#ffffff",
                        relief="flat")

        style.map("Treeview.Heading",
                  background=[('active', '#323b50')])

        # Configure severity-specific row styles
        style.configure("Critical.Treeview", background="#1c253a", foreground="#ff4757")  # Red
        style.configure("High.Treeview", background="#1c253a", foreground="#ffa502")  # Orange
        style.configure("Medium.Treeview", background="#1c253a", foreground="#f1c40f")  # Yellow
        style.configure("Low.Treeview", background="#1c253a", foreground="#2ed573")  # Green


def get_severity_color(severity):
    """Returns color code for severity levels"""
    colors = {
        "Critical": "#ff4757",  # Red
        "High": "#ffa502",  # Orange
        "Medium": "#f1c40f",  # Yellow
        "Low": "#2ed573"  # Green
    }
    return colors.get(severity, "#ffffff")


def load_threat_data(tree, threats):
    """Load threat data with colored severity rows"""
    # Clear existing data
    for item in tree.get_children():
        tree.delete(item)

    # Get the style object to create severity-specific row colors
    style = ttk.Style()

    # Insert data with severity-based row coloring
    for threat in threats:
        severity = threat['severity']

        # Insert the row with just the severity text
        item_id = tree.insert("", "end", values=(
            severity,  # Just the severity text
            threat["id"],
            threat["timestamp"],
            threat["type"],
            threat["client_machine"],
            threat["description"],
            threat["action_taken"]
        ))

        # Apply row-based color styling based on severity
        if severity == "Critical":
            tree.set(item_id, "severity", "Critical")
            # Create and apply critical row style
            style.configure("Critical.Treeview",
                            background="#4a1d1d",  # Dark red background
                            foreground="#ff6b6b")  # Light red text
            tree.item(item_id, tags=("critical",))
        elif severity == "High":
            tree.set(item_id, "severity", "High")
            style.configure("High.Treeview",
                            background="#4a3d1d",  # Dark orange background
                            foreground="#ffa726")  # Orange text
            tree.item(item_id, tags=("high",))
        elif severity == "Medium":
            tree.set(item_id, "severity", "Medium")
            style.configure("Medium.Treeview",
                            background="#4a4a1d",  # Dark yellow background
                            foreground="#ffeb3b")  # Yellow text
            tree.item(item_id, tags=("medium",))
        elif severity == "Low":
            tree.set(item_id, "severity", "Low")
            style.configure("Low.Treeview",
                            background="#1d4a1d",  # Dark green background
                            foreground="#66bb6a")  # Light green text
            tree.item(item_id, tags=("low",))

    # Configure tag-based styling for each severity level
    tree.tag_configure("critical", background="#4a1d1d", foreground="#ff6b6b")
    tree.tag_configure("high", background="#4a3d1d", foreground="#ffa726")
    tree.tag_configure("medium", background="#4a4a1d", foreground="#ffeb3b")
    tree.tag_configure("low", background="#1d4a1d", foreground="#66bb6a")


def open_threatlogs_page(parent_frame):
    """
    Threat logs page with colored severity indicators
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Threat Logs",
        font=("Roboto", 24, "bold"),
        text_color="#e9e8e8"
    )
    title.pack(anchor="w", padx=12, pady=12)

    # Create a frame for the filter controls
    filter_frame = customtkinter.CTkFrame(parent_frame, fg_color="#22232e")
    filter_frame.pack(fill="x", padx=20, pady=10)

    # Create filter controls
    # 1. Severity Filter
    severity_label = customtkinter.CTkLabel(filter_frame, text="Severity:", text_color="#e9e8e8")
    severity_label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="w")

    severities = ["All", "Critical", "High", "Medium", "Low"]
    severity_var = tk.StringVar(value="All")
    severity_dropdown = customtkinter.CTkOptionMenu(
        filter_frame,
        values=severities,
        variable=severity_var,
        width=150
    )
    severity_dropdown.grid(row=0, column=1, padx=5, pady=10, sticky="w")

    # 2. Date Filter
    date_label = customtkinter.CTkLabel(filter_frame, text="Date:", text_color="#e9e8e8")
    date_label.grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")

    date_ranges = ["All", "Today", "Last 3 Days", "Last Week", "Last Month"]
    date_var = tk.StringVar(value="All")
    date_dropdown = customtkinter.CTkOptionMenu(
        filter_frame,
        values=date_ranges,
        variable=date_var,
        width=150
    )
    date_dropdown.grid(row=0, column=3, padx=5, pady=10, sticky="w")

    # Create scrollable treeview for threat logs
    tree_frame = ScrollableTreeView(parent_frame)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Configure the treeview columns
    tree = tree_frame.tree
    columns = ("severity", "id", "timestamp", "type", "client_machine", "description", "action")
    tree["columns"] = columns
    tree["show"] = "headings"

    # Define column headings
    tree.heading("severity", text="Severity")
    tree.heading("id", text="ID")
    tree.heading("timestamp", text="Timestamp")
    tree.heading("type", text="Threat Type")
    tree.heading("client_machine", text="Client Machine")
    tree.heading("description", text="Description")
    tree.heading("action", text="Action Taken")

    # Set column widths with center alignment
    tree.column("severity", width=140, minwidth=140, anchor="center")
    tree.column("id", width=80, minwidth=80, anchor="center")
    tree.column("timestamp", width=150, minwidth=150, anchor="center")
    tree.column("type", width=150, minwidth=150, anchor="center")
    tree.column("client_machine", width=150, minwidth=150, anchor="center")
    tree.column("description", width=250, minwidth=250, anchor="center")
    tree.column("action", width=200, minwidth=200, anchor="center")

    # Create a details frame for displaying threat details when clicking on a row
    details_frame = customtkinter.CTkFrame(parent_frame, fg_color="#22232e")
    details_frame.pack(fill="x", padx=20, pady=10)

    # Initially hide the details frame
    details_frame.pack_forget()

    # Details label
    details_title = customtkinter.CTkLabel(
        details_frame,
        text="Threat Details",
        font=("Roboto", 18, "bold"),
        text_color="#e9e8e8"
    )
    details_title.pack(anchor="w", padx=15, pady=(15, 10))

    # Create frames for different sections of details
    machine_info_frame = customtkinter.CTkFrame(details_frame, fg_color="#22232e")
    machine_info_frame.pack(fill="x", padx=15, pady=5)

    affected_files_frame = customtkinter.CTkFrame(details_frame, fg_color="#22232e")
    affected_files_frame.pack(fill="x", padx=15, pady=5)

    # Apply Filter Button
    apply_button = customtkinter.CTkButton(
        filter_frame,
        text="Apply Filters",
        width=120,
        command=lambda: apply_filters(severity_var.get(), date_var.get())
    )
    apply_button.grid(row=0, column=4, padx=(20, 10), pady=10, sticky="e")

    # Function to apply filters
    def apply_filters(severity_filter, date_filter):
        # Clear current data
        for item in tree.get_children():
            tree.delete(item)

        # Apply filters
        filtered_threats = sample_threats.copy()

        # Filter by severity
        if severity_filter != "All":
            filtered_threats = [t for t in filtered_threats if t["severity"] == severity_filter]

        # Filter by date
        if date_filter != "All":
            current_date = datetime.datetime.now()

            if date_filter == "Today":
                date_limit = current_date - datetime.timedelta(days=1)
            elif date_filter == "Last 3 Days":
                date_limit = current_date - datetime.timedelta(days=3)
            elif date_filter == "Last Week":
                date_limit = current_date - datetime.timedelta(days=7)
            elif date_filter == "Last Month":
                date_limit = current_date - datetime.timedelta(days=30)
            else:
                date_limit = None

            if date_limit:
                filtered_threats = [
                    t for t in filtered_threats if
                    datetime.datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") >= date_limit
                ]

        # Load filtered data
        load_threat_data(tree, filtered_threats)

    # Function to show threat details
    def show_threat_details(event):
        # Get the selected item
        selection = tree.selection()
        if not selection:
            return

        # Get the threat ID from the selected item
        item = tree.item(selection[0])
        threat_id = item["values"][1]  # ID is in column 1

        # Find the corresponding threat data
        threat = next((t for t in sample_threats if t["id"] == threat_id), None)
        if not threat:
            return

        # Show the details frame
        details_frame.pack(fill="x", padx=20, pady=10)

        # Clear previous content in the info frames
        for widget in machine_info_frame.winfo_children():
            widget.destroy()

        for widget in affected_files_frame.winfo_children():
            widget.destroy()

        # Machine Info Section
        machine_title = customtkinter.CTkLabel(
            machine_info_frame,
            text="Machine Information",
            font=("Roboto", 16, "bold"),
            text_color="#e9e8e8"
        )
        machine_title.pack(anchor="w", padx=10, pady=(10, 5))

        # Machine info details
        machine_info = threat["machine_info"]

        info_grid = customtkinter.CTkFrame(machine_info_frame, fg_color="transparent")
        info_grid.pack(fill="x", padx=10, pady=5)

        # Client Machine
        customtkinter.CTkLabel(info_grid, text="Client Machine:", font=("Roboto", 12, "bold"),
                               text_color="#e9e8e8").grid(row=0, column=0,
                                                          sticky="w", padx=5,
                                                          pady=2)
        customtkinter.CTkLabel(info_grid, text=threat["client_machine"], text_color="#e9e8e8").grid(row=0, column=1,
                                                                                                    sticky="w", padx=5,
                                                                                                    pady=2)

        # OS
        customtkinter.CTkLabel(info_grid, text="Operating System:", font=("Roboto", 12, "bold"),
                               text_color="#e9e8e8").grid(row=1, column=0,
                                                          sticky="w", padx=5,
                                                          pady=2)
        customtkinter.CTkLabel(info_grid, text=machine_info["os"], text_color="#e9e8e8").grid(row=1, column=1,
                                                                                              sticky="w", padx=5,
                                                                                              pady=2)

        # IP
        customtkinter.CTkLabel(info_grid, text="IP Address:", font=("Roboto", 12, "bold"), text_color="#e9e8e8").grid(
            row=2, column=0,
            sticky="w", padx=5,
            pady=2)
        customtkinter.CTkLabel(info_grid, text=machine_info["ip"], text_color="#e9e8e8").grid(row=2, column=1,
                                                                                              sticky="w", padx=5,
                                                                                              pady=2)

        # Location
        customtkinter.CTkLabel(info_grid, text="Location:", font=("Roboto", 12, "bold"), text_color="#e9e8e8").grid(
            row=3, column=0,
            sticky="w", padx=5, pady=2)
        customtkinter.CTkLabel(info_grid, text=machine_info["location"], text_color="#e9e8e8").grid(row=3, column=1,
                                                                                                    sticky="w", padx=5,
                                                                                                    pady=2)

        # Affected Files Section
        files_title = customtkinter.CTkLabel(
            affected_files_frame,
            text="Affected Files",
            font=("Roboto", 16, "bold"),
            text_color="#e9e8e8"
        )
        files_title.pack(anchor="w", padx=10, pady=(10, 5))

        # Files list
        if threat["affected_files"]:
            files_list = customtkinter.CTkFrame(affected_files_frame, fg_color="transparent")
            files_list.pack(fill="x", padx=10, pady=5)

            for i, file_path in enumerate(threat["affected_files"]):
                file_frame = customtkinter.CTkFrame(files_list, fg_color="#283146")
                file_frame.pack(fill="x", pady=2)

                # Try to load appropriate icon based on file extension
                file_icon = None
                try:
                    # Get file extension
                    _, ext = os.path.splitext(file_path)
                    icon_path = os.path.join(assets_path, "icon", f"{ext[1:]}_icon.png")

                    if os.path.exists(icon_path):
                        icon_image = customtkinter.CTkImage(
                            light_image=Image.open(icon_path),
                            dark_image=Image.open(icon_path),
                            size=(16, 16)
                        )
                        file_icon = customtkinter.CTkLabel(file_frame, image=icon_image, text="")
                        file_icon.pack(side="left", padx=(5, 0))
                except Exception as e:
                    print(f"Failed to load icon: {e}")

                # File path label
                file_label = customtkinter.CTkLabel(file_frame, text=file_path, text_color="#e9e8e8")
                file_label.pack(side="left", padx=(10 if not file_icon else 5, 10), pady=5)
        else:
            no_files_label = customtkinter.CTkLabel(
                affected_files_frame,
                text="No files were directly affected by this threat.",
                text_color="#e9e8e8"
            )
            no_files_label.pack(anchor="w", padx=10, pady=5)

        # Action Taken Section
        action_title = customtkinter.CTkLabel(
            affected_files_frame,
            text="Action Taken",
            font=("Roboto", 16, "bold"),
            text_color="#e9e8e8"
        )
        action_title.pack(anchor="w", padx=10, pady=(10, 5))

        action_label = customtkinter.CTkLabel(
            affected_files_frame,
            text=threat["action_taken"],
            font=("Roboto", 13),
            text_color="#e9e8e8"
        )
        action_label.pack(anchor="w", padx=10, pady=5)

    # Bind click event to show details
    tree.bind("<<TreeviewSelect>>", show_threat_details)

    # Initially load all threat data
    load_threat_data(tree, sample_threats)