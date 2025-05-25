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
    title.pack(pady=(20, 10), anchor="w", padx=20)

    # Search and filter section - directly on parent frame
    search_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent", border_width=0)
    search_frame.pack(fill="x", padx=20, pady=10,)

    search_entry = customtkinter.CTkEntry(
        master=search_frame,
        placeholder_text="Search machines...",
        text_color="White",
        width=200
    )
    search_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

    search_button = customtkinter.CTkButton(
        master=search_frame,
        text="Search",
        width=80
    )
    search_button.grid(row=0, column=1, padx=5, pady=10, sticky="w")

    # Filter dropdown
    filter_var = tk.StringVar(value="All")
    filter_combobox = customtkinter.CTkComboBox(
        master=search_frame,
        width=120,
        values=["All", "Online", "Offline", "Compromised"],
        variable=filter_var
    )
    filter_combobox.grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")

    # Refresh button
    refresh_button = customtkinter.CTkButton(
        master=search_frame,
        text="Refresh List",
        width=120
    )
    refresh_button.grid(row=0, column=3, padx=(20, 10), pady=10, sticky="e")

    # Main content frame with two sections
    content_frame = customtkinter.CTkFrame(master=parent_frame, fg_color="transparent", border_width=0)
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Create two sections: Machine list on left, Details/Actions on right
    list_frame = customtkinter.CTkFrame(master=content_frame)
    list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    details_frame = customtkinter.CTkFrame(master=content_frame)
    details_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

    # ======= CLIENT MACHINE LIST SECTION =======
    list_label = customtkinter.CTkLabel(
        master=list_frame,
        text="Registered Machines",
        font=("Arial", 18, "bold")
    )
    list_label.pack(pady=10, anchor="w", padx=10)

    # Machines list with scrollbar - improved container with conditional scrollbar
    machines_list_container = customtkinter.CTkScrollableFrame(
        master=list_frame,
        width=400,
        height=500,
        scrollbar_button_color="#565B73",
        scrollbar_button_hover_color="#6B7089",border_width=0

    )

    machines_list_container.pack(fill="both", expand=True, padx=0, pady=0)


    # ======= MACHINE DETAILS SECTION =======
    details_label = customtkinter.CTkLabel(
        master=details_frame,
        text="Machine Details",
        font=("Arial", 18, "bold")
    )
    details_label.pack(pady=10, anchor="w", padx=10)

    # Machine info section - no extra container
    info_display_frame = customtkinter.CTkFrame(master=details_frame, fg_color="transparent", border_width=0)
    info_display_frame.pack(fill="x", padx=2, pady=10)

    # Initial empty state
    no_selection_label = customtkinter.CTkLabel(
        master=info_display_frame,
        text="Select a machine to view details",
        font=("Arial", 14)
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
            font=("Arial", 16, "bold")
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
            font=("Arial", 13, "bold")
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
                font=("Arial", 12, "bold"),
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 20))

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
            ).grid(row=row, column=1, sticky="w", pady=5)

        # Show the actions
        show_actions(machine)

    def show_actions(machine):
        """Display action buttons for the selected machine"""
        # Clear previous actions
        for widget in actions_display_frame.winfo_children():
            widget.destroy()

        # Show the actions frame
        actions_display_frame.pack(fill="x", padx=10, pady=10)

        # Title for actions section
        actions_title = customtkinter.CTkLabel(
            master=actions_display_frame,
            text="Remote Actions",
            font=("Arial", 16, "bold")
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

        # Row 3
        is_isolated = machine.get("isolated", False)
        isolate_text = "Connect to Network" if is_isolated else "Isolate Machine"
        isolate_button = customtkinter.CTkButton(
            master=buttons_grid,
            text=isolate_text,
            fg_color="#63003d" if not is_isolated else "#1b720f",
            command=lambda: handle_action("isolate", machine),
            width=140
        )
        isolate_button.grid(row=2, column=0, padx=(0, 10), pady=5, sticky="w")

        remote_button = customtkinter.CTkButton(
            master=buttons_grid,
            text="Remote Desktop",
            state="normal" if machine.get("status") == "Online" else "disabled",
            command=lambda: handle_action("remote", machine),
            width=140
        )
        remote_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

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

    def update_scrollbar_visibility():
        """Update scrollbar visibility based on content"""
        # Get the scrollable frame's internal frame
        inner_frame = machines_list_container._parent_canvas

        # Update the canvas to make sure scrollregion is current
        machines_list_container.update_idletasks()

        # Check if scrolling is needed
        canvas_height = inner_frame.winfo_height()
        scroll_height = inner_frame.bbox("all")

        if scroll_height and scroll_height[3] > canvas_height:
            # Content is larger than visible area, scrollbar should be visible
            machines_list_container._scrollbar.grid()
        else:
            # Content fits in visible area, hide scrollbar
            machines_list_container._scrollbar.grid_remove()

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

        # Display machines with clean design
        for machine in machines:
            # Create a clean frame for this machine row
            machine_frame = customtkinter.CTkFrame(
                master=machines_list_container,
                fg_color="#283146",
                corner_radius=8
            )
            machine_frame.pack(fill="x", pady=3, padx=(0,6))

            # Content container
            content_container = customtkinter.CTkFrame(machine_frame, fg_color="transparent", border_width=0)
            content_container.pack(fill="x", padx=10, pady=8)

            # Status indicator (colored dot)
            status = machine.get("status", "Offline")
            status_color = {
                "Online": "#1b720f",  # Green
                "Offline": "#748498",  # Gray
                "Compromised": "#63003d"  # Red
            }.get(status, "#748498")

            status_indicator = customtkinter.CTkFrame(
                master=content_container,
                width=10,
                height=10,
                corner_radius=5,
                fg_color=status_color

            )
            status_indicator.pack(side="left", padx=(0, 10))

            # Machine info container
            info_container = customtkinter.CTkFrame(content_container, fg_color="transparent", border_width=0)
            info_container.pack(side="left", fill="x", expand=True)

            # Machine name
            machine_name = customtkinter.CTkLabel(
                master=info_container,
                text=machine.get("username", "Unknown"),
                font=("Arial", 13, "bold"),
                anchor="w"
            )
            machine_name.pack(anchor="w")

            # Location and status info
            if machine.get("location"):
                location_text = f"{machine.get('location')} • {status}"
                location_label = customtkinter.CTkLabel(
                    master=info_container,
                    text=location_text,
                    font=("Arial", 11),
                    text_color="#9CA3AF",
                    anchor="w"
                )
                location_label.pack(anchor="w")

            # Alert count for compromised machines
            if status == "Compromised":
                threat_count = machine.get("threats_detected", 0)
                threat_label = customtkinter.CTkLabel(
                    master=content_container,
                    text=f"⚠️ {threat_count}",
                    font=("Arial", 12, "bold"),
                    text_color="#63003d"
                )
                threat_label.pack(side="right", padx=(10, 0))

            # Make the entire row clickable
            machine_frame.bind("<Button-1>", lambda e, m=machine: select_machine(m))
            for widget in machine_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, m=machine: select_machine(m))
                for subwidget in widget.winfo_children():
                    subwidget.bind("<Button-1>", lambda e, m=machine: select_machine(m))

        # Update scrollbar visibility after adding all machines
        machines_list_container.after(100, update_scrollbar_visibility)

    def select_machine(machine):
        """Handle machine selection from the list"""
        # Store selected machine ID for reference
        handle_action.selected_machine = machine["id"]

        # Show the machine details
        show_machine_details(machine)

    # Set up event handlers
    search_button.configure(command=refresh_machines_list)
    search_entry.bind("<Return>", lambda event: refresh_machines_list())
    filter_combobox.configure(command=lambda _: refresh_machines_list())
    refresh_button.configure(command=refresh_machines_list)

    # Initial population of the machines list
    refresh_machines_list()