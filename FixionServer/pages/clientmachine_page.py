import customtkinter
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import random  # For demo purposes to simulate machine statuses


def open_clientmachine_page(parent_frame):
    """
    Client machine management page for anti-virus system
    Shows connected machines, their status, and allows remote actions
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Client Machine Management",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=20, anchor="w", padx=15)

    # Main content frame with two sections
    content_frame = customtkinter.CTkFrame(master=parent_frame)
    content_frame.pack(fill="both", expand=True, padx=15, pady=10)

    # Create two sections: Machine list on left, Details/Actions on right
    list_frame = customtkinter.CTkFrame(master=content_frame)
    list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    details_frame = customtkinter.CTkFrame(master=content_frame)
    details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ======= CLIENT MACHINE LIST SECTION =======
    list_label = customtkinter.CTkLabel(
        master=list_frame,
        text="Registered Machines",
        font=("Arial", 18, "bold")
    )
    list_label.pack(pady=10, anchor="w", padx=10)

    # Search and filter section
    search_frame = customtkinter.CTkFrame(master=list_frame, fg_color="transparent")
    search_frame.pack(fill="x", padx=10, pady=(5, 10))

    search_entry = customtkinter.CTkEntry(
        master=search_frame,
        placeholder_text="Search machines...",
        width=200
    )
    search_entry.pack(side="left", padx=(0, 10))

    search_button = customtkinter.CTkButton(
        master=search_frame,
        text="Search",
        width=80
    )
    search_button.pack(side="left", padx=(0, 10))

    # Filter dropdown
    filter_var = tk.StringVar(value="All")
    filter_combobox = customtkinter.CTkComboBox(
        master=search_frame,
        width=120,
        values=["All", "Online", "Offline", "Compromised"],
        variable=filter_var
    )
    filter_combobox.pack(side="left")

    # Machines list with scrollbar
    machines_list_container = customtkinter.CTkScrollableFrame(
        master=list_frame,
        width=400,
        height=500
    )
    machines_list_container.pack(fill="both", expand=True, padx=10, pady=10)

    # ======= MACHINE DETAILS SECTION =======
    details_label = customtkinter.CTkLabel(
        master=details_frame,
        text="Machine Details",
        font=("Arial", 18, "bold")
    )
    details_label.pack(pady=10, anchor="w", padx=10)

    # Machine info section
    info_frame = customtkinter.CTkFrame(master=details_frame)
    info_frame.pack(fill="x", padx=10, pady=10)

    # Initial empty state
    no_selection_label = customtkinter.CTkLabel(
        master=info_frame,
        text="Select a machine to view details",
        font=("Arial", 14)
    )
    no_selection_label.pack(pady=20)

    # Status section - initially hidden
    status_frame = customtkinter.CTkFrame(master=details_frame)

    # Actions section - initially hidden
    actions_frame = customtkinter.CTkFrame(master=details_frame)

    # ======= HELPER FUNCTIONS =======

    def load_machines():
        """Load machine data from JSON file"""
        try:
            # If users.json exists, load and filter for client machines
            if os.path.exists('users.json'):
                with open('users.json', 'r') as file:
                    all_users = json.load(file)
                    # Filter for client machines only
                    return [user for user in all_users if user.get("role") == "client machine"]

            # If specific machines file exists, load it
            if os.path.exists('machines.json'):
                with open('machines.json', 'r') as file:
                    return json.load(file)

            # Return some demo data if no files found
            return get_demo_machines()
        except Exception as e:
            print(f"Error loading machines: {e}")
            return get_demo_machines()

    def get_demo_machines():
        """Generate demo machine data for testing"""
        statuses = ["Online", "Offline", "Compromised"]
        os_types = ["Windows 11", "Windows 10", "Windows Server 2022", "Linux Ubuntu", "macOS"]
        locations = ["Main Office", "Branch Office", "Remote", "Development", "Finance Dept", "HR Dept"]

        demo_machines = []
        for i in range(1, 11):
            # Simulate different statuses with weighted probabilities
            status_weights = [0.6, 0.3, 0.1]  # 60% online, 30% offline, 10% compromised
            status = random.choices(statuses, weights=status_weights)[0]

            machine = {
                "id": i,
                "username": f"PC-{100 + i}",
                "first_name": f"PC-{100 + i}",
                "last_name": "Computer",
                "role": "client machine",
                "type": "client",
                "active": True,
                "location": random.choice(locations),
                "status": status,
                "os": random.choice(os_types),
                "last_scan": (datetime.now().replace(
                    hour=random.randint(0, 23),
                    minute=random.randint(0, 59)
                )).strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": f"192.168.1.{random.randint(2, 254)}",
                "threats_detected": random.randint(0, 5) if status == "Compromised" else 0,
                "av_version": f"1.{random.randint(0, 9)}.{random.randint(0, 99)}"
            }
            demo_machines.append(machine)

        return demo_machines

    def show_machine_details(machine):
        """Display detailed information about the selected machine"""
        # Clear previous details
        for widget in info_frame.winfo_children():
            widget.destroy()

        # Create grid layout for machine info
        info_grid = customtkinter.CTkFrame(master=info_frame, fg_color="transparent")
        info_grid.pack(fill="both", expand=True, padx=10, pady=10)

        # Machine name header
        name_label = customtkinter.CTkLabel(
            master=info_grid,
            text=machine.get("username", "Unknown Machine"),
            font=("Arial", 16, "bold")
        )
        name_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Status with colored indicator
        status_text = machine.get("status", "Unknown")
        status_color = {
            "Online": "#1b720f",  # Green
            "Offline": "#748498",  # Gray
            "Compromised": "#63003d"  # Red
        }.get(status_text, "#748498")

        status_frame = customtkinter.CTkFrame(master=info_grid, fg_color="transparent")
        status_frame.grid(row=1, column=0, sticky="w", pady=5)

        status_indicator = customtkinter.CTkFrame(
            master=status_frame,
            width=12,
            height=12,
            corner_radius=6,
            fg_color=status_color
        )
        status_indicator.pack(side="left", padx=(0, 5))

        status_label = customtkinter.CTkLabel(
            master=status_frame,
            text=f"Status: {status_text}",
            font=("Arial", 12)
        )
        status_label.pack(side="left")

        # Details grid
        details = [
            ("Location:", machine.get("location", "Unknown")),
            ("IP Address:", machine.get("ip_address", "Unknown")),
            ("Operating System:", machine.get("os", "Unknown")),
            ("Anti-virus Version:", machine.get("av_version", "Unknown")),
            ("Last Scan:", machine.get("last_scan", "Never")),
            ("Threats Detected:", str(machine.get("threats_detected", 0)))
        ]

        for i, (label_text, value_text) in enumerate(details):
            row = i + 2  # Start after name and status

            # Label
            customtkinter.CTkLabel(
                master=info_grid,
                text=label_text,
                font=("Arial", 12, "bold"),
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=5)

            # Value
            value_color = "#ECEFF1"  # Default color
            if label_text == "Threats Detected:" and int(value_text) > 0:
                value_color = "#63003d"  # Red for threats

            customtkinter.CTkLabel(
                master=info_grid,
                text=value_text,
                font=("Arial", 12),
                text_color=value_color,
                anchor="w"
            ).grid(row=row, column=1, sticky="w", pady=5, padx=10)

        # Show the actions frame
        show_actions(machine)

    def show_actions(machine):
        """Display action buttons for the selected machine"""
        # Clear previous actions
        for widget in actions_frame.winfo_children():
            widget.destroy()

        # Show the actions frame
        actions_frame.pack(fill="x", padx=10, pady=10)

        # Title for actions section
        actions_title = customtkinter.CTkLabel(
            master=actions_frame,
            text="Remote Actions",
            font=("Arial", 16, "bold")
        )
        actions_title.pack(pady=(5, 10), anchor="w", padx=10)

        # Action buttons
        actions_buttons_frame = customtkinter.CTkFrame(master=actions_frame, fg_color="transparent")
        actions_buttons_frame.pack(fill="x", padx=10, pady=5)

        # Run scan button
        scan_button = customtkinter.CTkButton(
            master=actions_buttons_frame,
            text="Run Full Scan",
            command=lambda: handle_action("scan", machine)
        )
        scan_button.grid(row=0, column=0, padx=5, pady=5)

        # Quick scan button
        quick_scan_button = customtkinter.CTkButton(
            master=actions_buttons_frame,
            text="Quick Scan",
            command=lambda: handle_action("quick_scan", machine)
        )
        quick_scan_button.grid(row=0, column=1, padx=5, pady=5)

        # Update button
        update_button = customtkinter.CTkButton(
            master=actions_buttons_frame,
            text="Update Definitions",
            command=lambda: handle_action("update", machine)
        )
        update_button.grid(row=1, column=0, padx=5, pady=5)

        # Trigger rollback button
        rollback_button = customtkinter.CTkButton(
            master=actions_buttons_frame,
            text="Trigger Rollback",
            command=lambda: handle_action("rollback", machine)
        )
        rollback_button.grid(row=1, column=1, padx=5, pady=5)

        # Isolate/Connect button
        is_isolated = machine.get("isolated", False)
        isolate_text = "Connect to Network" if is_isolated else "Isolate Machine"
        isolate_button = customtkinter.CTkButton(
            master=actions_buttons_frame,
            text=isolate_text,
            fg_color="#63003d" if not is_isolated else "#1b720f",
            command=lambda: handle_action("isolate", machine)
        )
        isolate_button.grid(row=2, column=0, padx=5, pady=5)

        # Remote desktop button - disabled if machine is offline
        remote_button = customtkinter.CTkButton(
            master=actions_buttons_frame,
            text="Remote Desktop",
            state="normal" if machine.get("status") == "Online" else "disabled",
            command=lambda: handle_action("remote", machine)
        )
        remote_button.grid(row=2, column=1, padx=5, pady=5)

    def handle_action(action, machine):
        """Handle the remote actions for machines"""
        machine_name = machine.get("username", "Unknown")

        actions = {
            "scan": f"Initiating full scan on {machine_name}...",
            "quick_scan": f"Initiating quick scan on {machine_name}...",
            "update": f"Updating virus definitions on {machine_name}...",
            "rollback": f"WARNING: About to rollback {machine_name} to previous system snapshot.",
            "isolate": "isolate_action",  # Special handling
            "remote": f"Establishing remote desktop connection to {machine_name}..."
        }

        # Special handling for isolate action
        if action == "isolate":
            currently_isolated = machine.get("isolated", False)
            if currently_isolated:
                message = f"Reconnecting {machine_name} to network..."
                machine["isolated"] = False
            else:
                message = f"WARNING: About to isolate {machine_name} from network. Continue?"
                confirm = messagebox.askyesno("Confirm Isolation", message)
                if confirm:
                    message = f"Isolating {machine_name} from network..."
                    machine["isolated"] = True
                else:
                    return
        else:
            message = actions[action]

            # Confirmation for potentially destructive actions
            if action == "rollback":
                confirm = messagebox.askyesno("Confirm Rollback", message + " Continue?")
                if not confirm:
                    return

        # Show action in progress
        messagebox.showinfo("Action Initiated", message)

        # For demo: update the machines list to reflect changes
        refresh_machines_list()

        # If the current machine is still selected, refresh its details view
        if hasattr(handle_action, "selected_machine") and handle_action.selected_machine == machine["id"]:
            show_machine_details(machine)

    def refresh_machines_list():
        """Refresh the list of machines with current filter applied"""
        # Clear current list
        for widget in machines_list_container.winfo_children():
            widget.destroy()

        # Load machines
        machines = load_machines()

        # Apply search filter if any
        search_term = search_entry.get().lower()
        if search_term:
            machines = [m for m in machines if
                        search_term in m.get("username", "").lower() or
                        search_term in m.get("location", "").lower()]

        # Apply status filter if not "All"
        status_filter = filter_var.get()
        if status_filter != "All":
            machines = [m for m in machines if m.get("status") == status_filter]

        # Sort by status priority: Compromised > Online > Offline
        def sort_key(machine):
            status = machine.get("status", "")
            if status == "Compromised":
                return 0
            elif status == "Online":
                return 1
            else:  # Offline or any other status
                return 2

        machines.sort(key=sort_key)

        # Display machines
        for machine in machines:
            # Create a frame for this machine row
            machine_frame = customtkinter.CTkFrame(master=machines_list_container)
            machine_frame.pack(fill="x", pady=5, padx=2)

            # Status indicator (colored dot)
            status = machine.get("status", "Offline")
            status_color = {
                "Online": "#1b720f",  # Green
                "Offline": "#748498",  # Gray
                "Compromised": "#63003d"  # Red
            }.get(status, "#748498")

            status_indicator = customtkinter.CTkFrame(
                master=machine_frame,
                width=12,
                height=12,
                corner_radius=6,
                fg_color=status_color
            )
            status_indicator.pack(side="left", padx=10)

            # Machine name
            machine_name = customtkinter.CTkLabel(
                master=machine_frame,
                text=machine.get("username", "Unknown"),
                font=("Arial", 12, "bold")
            )
            machine_name.pack(side="left", padx=5)

            # Location if available
            if machine.get("location"):
                location_text = f"({machine.get('location')})"
                location_label = customtkinter.CTkLabel(
                    master=machine_frame,
                    text=location_text,
                    font=("Arial", 12)
                )
                location_label.pack(side="left", padx=5)

            # Alert count for compromised machines
            if status == "Compromised":
                threat_count = machine.get("threats_detected", 0)
                threat_label = customtkinter.CTkLabel(
                    master=machine_frame,
                    text=f"⚠️ {threat_count}",
                    font=("Arial", 12, "bold"),
                    text_color="#63003d"
                )
                threat_label.pack(side="right", padx=10)

            # Make the entire row clickable
            machine_frame.bind("<Button-1>", lambda e, m=machine: select_machine(m))
            for widget in machine_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, m=machine: select_machine(m))

    def select_machine(machine):
        """Handle machine selection from the list"""
        # Store selected machine ID for reference
        handle_action.selected_machine = machine["id"]

        # Clear the no-selection message
        for widget in info_frame.winfo_children():
            widget.destroy()

        # Show the machine details
        show_machine_details(machine)

        # Make the details and actions frames visible
        status_frame.pack(fill="x", padx=10, pady=10)
        actions_frame.pack(fill="x", padx=10, pady=10)

    # Set up event handlers
    search_button.configure(command=refresh_machines_list)
    search_entry.bind("<Return>", lambda event: refresh_machines_list())
    filter_combobox.configure(command=lambda _: refresh_machines_list())

    # Initial population of the machines list
    refresh_machines_list()

    # Add refresh button at the bottom of the list
    refresh_button = customtkinter.CTkButton(
        master=list_frame,
        text="Refresh List",
        width=120,
        command=refresh_machines_list
    )
    refresh_button.pack(pady=10)