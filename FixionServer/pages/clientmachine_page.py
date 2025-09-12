import customtkinter
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import random  # For demo purposes to simulate machine statuses


def open_clientmachine_page(parent_frame):
    """
    Clean client machine management page for anti-virus system
    Shows connected machines in grid view with status and name only
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Client Machine Management",
        font=("Roboto", 24, "bold"),
        text_color="#e9e8e8"
    )
    title.pack(anchor="w", padx=(12,0), pady= (12,0))

    # Search and filter section - directly on parent frame
    search_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent", border_width=0)
    search_frame.pack(fill="x", padx=(30,0), pady= (18,0))

    search_entry = customtkinter.CTkEntry(
        master=search_frame,
        placeholder_text="Search machines...",
        width=200,
        border_width=0,
        fg_color="#22222f",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12
    )
    search_entry.grid(row=0, column=0, sticky="w")

    search_button = customtkinter.CTkButton(
        master=search_frame,
        text="Search",
        width=80,
        corner_radius=28
    )
    search_button.grid(row=0, column=1, padx=(5,0), sticky="w")

    # Filter dropdown
    filter_var = tk.StringVar(value="All")
    filter_combobox = customtkinter.CTkComboBox(
        master=search_frame,
        width=120,
        values=["All", "Online", "Offline", "Compromised"],
        variable=filter_var,
        border_width=0,
        fg_color="#22222f",
        button_color="#22222f",
        dropdown_fg_color="#22222f",
        dropdown_font=("Roboto Medium", 12),
        dropdown_text_color="#e9e8e8",
        corner_radius=12,
        text_color="#b1b4c9",

    )
    filter_combobox.grid(row=0, column=2, padx=(20, 5), sticky="w")

    # Refresh button
    refresh_button = customtkinter.CTkButton(
        master=search_frame,
        text="Refresh List",
        width=120,
        corner_radius=28
    )
    refresh_button.grid(row=0, column=3, padx=(20, 10), sticky="e")

    # Main content frame with two sections
    content_frame = customtkinter.CTkFrame(master=parent_frame,fg_color="#15141b")
    content_frame.pack(fill="both", expand=True, padx=30,pady=12)

    # Create two sections: Machine grid on left, Details/Actions on right
    list_frame = customtkinter.CTkFrame(master=content_frame, fg_color="#22232e",border_width=0, corner_radius=20 )
    list_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

    details_frame = customtkinter.CTkFrame(master=content_frame, fg_color="#22232e",border_width=0, corner_radius=20 )
    details_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

    # ======= CLIENT MACHINE GRID SECTION =======
    list_label = customtkinter.CTkLabel(
        master=list_frame,
        text="Registered Machines",
        text_color="#e9e8e8",
        font=("Roboto", 18, "bold")
    )
    list_label.pack(pady=10, anchor="w", padx=10)

    # Machines grid with scrollbar
    machines_grid_container = customtkinter.CTkScrollableFrame(
        master=list_frame,
        width=400,
        height=500,
        scrollbar_button_color="#565B73",
        scrollbar_button_hover_color="#6B7089",
        border_width=0,
        fg_color="#22222f"
    )
    machines_grid_container.pack(fill="both", expand=True, padx=4, pady=(0,20))

    # ======= MACHINE DETAILS SECTION =======
    details_label = customtkinter.CTkLabel(
        master=details_frame,
        text="Machine Details",
        text_color="#e9e8e8",
        font=("Roboto", 18, "bold")
    )
    details_label.pack(pady=10, anchor="w", padx=10)

    # Machine info section - no extra container
    info_display_frame = customtkinter.CTkFrame(master=details_frame, fg_color="transparent", border_width=0,)
    info_display_frame.pack(fill="x", padx=2, pady=10)

    # Initial empty state
    no_selection_label = customtkinter.CTkLabel(
        master=info_display_frame,
        text="Select a machine to view details",
        text_color="#e9e8e8",
        font=("Roboto", 14)
    )
    no_selection_label.pack(pady=20)

    # Actions section - clean layout
    actions_display_frame = customtkinter.CTkFrame(master=details_frame, fg_color="transparent", border_width=0)

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
        for widget in info_display_frame.winfo_children():
            widget.destroy()

        # Machine name header
        name_label = customtkinter.CTkLabel(
            master=info_display_frame,
            text=machine.get("username", "Unknown Machine"),
            font=("Roboto", 16, "bold"),
            text_color="#e9e8e8"
        )
        name_label.pack(anchor="w", pady=(10, 15), padx=12)

        # Create clean grid layout for machine info
        info_grid = customtkinter.CTkFrame(master=info_display_frame, fg_color="transparent", border_width=0)
        info_grid.pack(fill="x", pady=2, padx=12)

        # Status with colored indicator - clean design
        status_text = machine.get("status", "Unknown")
        status_color = {
            "Online": "#1b720f",  # Green
            "Offline": "#748498",  # Gray
            "Compromised": "#63003d"  # Red
        }.get(status_text, "#748498")

        status_container = customtkinter.CTkFrame(master=info_grid, fg_color="transparent", border_width=0)
        status_container.grid(row=0, column=0, columnspan=2, sticky="w", pady=0)

        status_indicator = customtkinter.CTkFrame(
            master=status_container,
            width=12,
            height=12,
            corner_radius=6,
            fg_color=status_color
        )
        status_indicator.pack(side="left", padx=(0, 8))

        status_label = customtkinter.CTkLabel(
            master=status_container,
            text=f"Status: {status_text}",
            font=("Roboto", 14, "bold"),
            text_color="#e9e8e8"
        )
        status_label.pack(side="left")

        # Details in clean grid layout
        details = [
            ("Location:", machine.get("location", "Unknown")),
            ("IP Address:", machine.get("ip_address", "Unknown")),
            ("Operating System:", machine.get("os", "Unknown")),
            ("Anti-virus Version:", machine.get("av_version", "Unknown")),
            ("Last Scan:", machine.get("last_scan", "Never")),
            ("Threats Detected:", str(machine.get("threats_detected", 0)))
        ]

        for i, (label_text, value_text) in enumerate(details):
            row = i + 1  # Start after status

            # Label
            customtkinter.CTkLabel(
                master=info_grid,
                text=label_text,
                text_color="#e9e8e8",
                font=("Roboto", 12, "bold"),
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 20))

            # Value
            value_color = "#ECEFF1"  # Default color
            if label_text == "Threats Detected:" and int(value_text) > 0:
                value_color = "#63003d"  # Red for threats

            customtkinter.CTkLabel(
                master=info_grid,
                text=value_text,
                font=("Roboto", 12),
                text_color=value_color,
                anchor="w"
            ).grid(row=row, column=1, sticky="w", pady=5)

        # Show the actions
        show_actions(machine)

    def show_actions(machine):
        """Display action buttons for the selected machine - without isolate button"""
        # Clear previous actions
        for widget in actions_display_frame.winfo_children():
            widget.destroy()

        # Show the actions frame
        actions_display_frame.pack(fill="x", padx=10, pady=10)

        # Title for actions section
        actions_title = customtkinter.CTkLabel(
            master=actions_display_frame,
            text="Remote Actions",
            font=("Roboto", 16, "bold"),
            text_color="#e9e8e8"
        )
        actions_title.pack(anchor="w", pady=(0, 15))

        # Action buttons in clean grid
        buttons_grid = customtkinter.CTkFrame(master=actions_display_frame, fg_color="transparent", border_width=0)
        buttons_grid.pack(fill="x")

        # Row 1
        scan_button = customtkinter.CTkButton(
            master=buttons_grid,
            text="Run Full Scan",
            command=lambda: handle_action("scan", machine),
            width=140
        )
        scan_button.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        quick_scan_button = customtkinter.CTkButton(
            master=buttons_grid,
            text="Quick Scan",
            command=lambda: handle_action("quick_scan", machine),
            width=140
        )
        quick_scan_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Row 2
        update_button = customtkinter.CTkButton(
            master=buttons_grid,
            text="Update Definitions",
            command=lambda: handle_action("update", machine),
            width=140
        )
        update_button.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")

        rollback_button = customtkinter.CTkButton(
            master=buttons_grid,
            text="Trigger Rollback",
            command=lambda: handle_action("rollback", machine),
            width=140
        )
        rollback_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Note: Isolate machine button has been removed

    def handle_action(action, machine):
        """Handle the remote actions for machines"""
        machine_name = machine.get("username", "Unknown")

        actions = {
            "scan": f"Initiating full scan on {machine_name}...",
            "quick_scan": f"Initiating quick scan on {machine_name}...",
            "update": f"Updating virus definitions on {machine_name}...",
            "rollback": f"WARNING: About to rollback {machine_name} to previous system snapshot.",
            "remote": f"Establishing remote desktop connection to {machine_name}..."
        }

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
        """Refresh the grid of machines with current filter applied"""
        # Clear current grid
        for widget in machines_grid_container.winfo_children():
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

        # Create grid layout - 5 columns
        columns = 5
        for i, machine in enumerate(machines):
            row = i // columns
            col = i % columns

            # Create compact machine card
            machine_card = customtkinter.CTkFrame(
                master=machines_grid_container,
                fg_color="#283146",
                corner_radius=12,
                width=120,
                height=80
            )
            machine_card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")

            # Configure column weights for even spacing
            machines_grid_container.grid_columnconfigure(col, weight=1)

            # Status indicator at top
            status = machine.get("status", "Offline")
            status_color = {
                "Online": "#1b720f",  # Green
                "Offline": "#748498",  # Gray
                "Compromised": "#63003d"  # Red
            }.get(status, "#748498")

            # Status indicator circle
            status_indicator = customtkinter.CTkFrame(
                master=machine_card,
                width=12,
                height=12,
                corner_radius=12,
                fg_color=status_color
            )
            status_indicator.pack(pady=(8, 4))

            # Machine name
            machine_name = customtkinter.CTkLabel(
                master=machine_card,
                text=machine.get("username", "Unknown"),
                font=("Roboto", 12, "bold"),
                text_color="#e9e8e8",
                wraplength=100
            )
            machine_name.pack(pady=(0, 4))

            # Status text
            status_label = customtkinter.CTkLabel(
                master=machine_card,
                text=status,
                font=("Roboto", 10),
                text_color="#e9e8e8"
            )
            status_label.pack(pady=(0, 8))

            # Add threat indicator for compromised machines
            if status == "Compromised":
                threat_count = machine.get("threats_detected", 0)
                threat_indicator = customtkinter.CTkLabel(
                    master=machine_card,
                    text=f"⚠ {threat_count}",
                    font=("Roboto", 9),
                    text_color="#63003d"
                )
                threat_indicator.pack()

            # Make the entire card clickable
            def make_click_handler(m):
                return lambda e: select_machine(m)

            machine_card.bind("<Button-1>", make_click_handler(machine))
            for widget in machine_card.winfo_children():
                widget.bind("<Button-1>", make_click_handler(machine))

    def select_machine(machine):
        """Handle machine selection from the grid"""
        # Store selected machine ID for reference
        handle_action.selected_machine = machine["id"]

        # Show the machine details
        show_machine_details(machine)

    # Set up event handlers
    search_button.configure(command=refresh_machines_list)
    search_entry.bind("<Return>", lambda event: refresh_machines_list())
    filter_combobox.configure(command=lambda _: refresh_machines_list())
    refresh_button.configure(command=refresh_machines_list)

    # Initial population of the machines grid
    refresh_machines_list()