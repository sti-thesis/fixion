import customtkinter
import tkinter as tk
from datetime import datetime, timedelta
import random
import json


def open_snapshot_page(parent_frame):
    """
    Snapshots & Rollbacks page with timeline view and rollback functionality
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Snapshot",
        font=("Roboto", 24, "bold"),
        text_color= "#e9e8e8"
    )
    title.pack(anchor="w", padx=12, pady= 12)

    # Create tabs for different sections
    tab_view = customtkinter.CTkTabview(master=parent_frame, fg_color="#22222f")
    tab_view.pack(fill="both", expand=True, padx=20, pady=10)

    tab_timeline = tab_view.add("Snapshot Timeline")
    tab_settings = tab_view.add("Settings")

    # === Timeline Tab ===
    # Machine selection frame
    machine_frame = customtkinter.CTkFrame(tab_timeline)
    machine_frame.pack(fill="x", padx=10, pady=10)

    machine_label = customtkinter.CTkLabel(
        master=machine_frame,
        text="Select Machine:",
        font=("Arial", 14)
    )
    machine_label.pack(side="left", padx=10)

    # Load machines from users.json file
    def load_client_machines():
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
                # Filter only client machines that are active
                clients = [user.get('username') for user in users
                           if user.get('role') == 'client machine' and user.get('active', True)]
                if not clients:  # If no clients found, provide a placeholder
                    return ["No clients available"]
                return clients
        except (FileNotFoundError, json.JSONDecodeError):
            return ["No clients available"]  # Return a placeholder if file not found or invalid

    machines = load_client_machines()
    machine_var = tk.StringVar(value=machines[0] if machines else "")

    machine_menu = customtkinter.CTkOptionMenu(
        master=machine_frame,
        values=machines,
        variable=machine_var,
        command=lambda x: refresh_snapshots(x)
    )
    machine_menu.pack(side="left", padx=10)

    refresh_button = customtkinter.CTkButton(
        master=machine_frame,
        text="Refresh",
        width=100,
        command=lambda: refresh_machine_list()
    )
    refresh_button.pack(side="right", padx=10)

    def refresh_machine_list():
        """Refresh the list of machines from users.json"""
        updated_machines = load_client_machines()
        current_machine = machine_var.get()

        # Update the option menu with new machines
        machine_menu.configure(values=updated_machines)

        # If current selection is still in the list, keep it selected
        if current_machine in updated_machines:
            machine_var.set(current_machine)
        else:
            machine_var.set(updated_machines[0] if updated_machines else "")

        # Refresh snapshots for the selected machine
        refresh_snapshots(machine_var.get())

    # Timeline frame with scrollable content
    timeline_frame = customtkinter.CTkScrollableFrame(tab_timeline)
    timeline_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Details frame at the bottom
    details_frame = customtkinter.CTkFrame(tab_timeline)
    details_frame.pack(fill="x", padx=10, pady=10)

    details_title = customtkinter.CTkLabel(
        master=details_frame,
        text="Snapshot Details",
        font=("Arial", 16, "bold")
    )
    details_title.pack(anchor="w", padx=10, pady=5)

    details_content = customtkinter.CTkLabel(
        master=details_frame,
        text="Select a snapshot to view details",
        font=("Arial", 12),
        justify="left",
        anchor="w"
    )
    details_content.pack(anchor="w", padx=10, pady=5, fill="x")

    rollback_button = customtkinter.CTkButton(
        master=details_frame,
        text="Rollback to Selected Snapshot",
        state="disabled",
        command=lambda: perform_rollback()
    )
    rollback_button.pack(anchor="e", padx=10, pady=10)

    # === Settings Tab ===
    settings_frame = customtkinter.CTkFrame(tab_settings)
    settings_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Snapshot frequency setting
    frequency_label = customtkinter.CTkLabel(
        master=settings_frame,
        text="Snapshot Frequency:",
        font=("Arial", 14)
    )
    frequency_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    frequency_options = ["Every 12 hours", "Daily", "Every 2 days", "Weekly"]
    frequency_var = tk.StringVar(value=frequency_options[1])

    frequency_menu = customtkinter.CTkOptionMenu(
        master=settings_frame,
        values=frequency_options,
        variable=frequency_var
    )
    frequency_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Retention policy setting
    retention_label = customtkinter.CTkLabel(
        master=settings_frame,
        text="Retention Policy:",
        font=("Arial", 14)
    )
    retention_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    retention_options = ["Keep 7 days", "Keep 14 days", "Keep 30 days", "Keep 90 days"]
    retention_var = tk.StringVar(value=retention_options[2])

    retention_menu = customtkinter.CTkOptionMenu(
        master=settings_frame,
        values=retention_options,
        variable=retention_var
    )
    retention_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Auto-snapshot setting
    auto_snapshot = tk.BooleanVar(value=True)
    auto_checkbox = customtkinter.CTkCheckBox(
        master=settings_frame,
        text="Enable automatic snapshots",
        variable=auto_snapshot
    )
    auto_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    # Pre-rollback snapshot setting
    pre_rollback = tk.BooleanVar(value=True)
    pre_rollback_checkbox = customtkinter.CTkCheckBox(
        master=settings_frame,
        text="Create snapshot before rollback",
        variable=pre_rollback
    )
    pre_rollback_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    # Save settings button
    save_button = customtkinter.CTkButton(
        master=settings_frame,
        text="Save Settings",
        command=lambda: save_settings()
    )
    save_button.grid(row=4, column=1, padx=10, pady=20, sticky="e")

    # Function to create a single snapshot item in the timeline
    def create_snapshot_item(parent, date, status, size, description):
        # Status colors
        status_colors = {
            "Clean": "#1b720f",  # Green
            "Potential Threat": "#ff9800",  # Orange
            "Corrupted": "#ff0000"  # Red
        }

        item_frame = customtkinter.CTkFrame(parent)
        item_frame.pack(fill="x", padx=5, pady=5)

        # Status indicator (colored circle)
        status_indicator = customtkinter.CTkFrame(
            master=item_frame,
            width=15,
            height=15,
            corner_radius=10,
            fg_color=status_colors.get(status, "#808080")
        )
        status_indicator.pack(side="left", padx=10)

        # Date and time
        date_label = customtkinter.CTkLabel(
            master=item_frame,
            text=date,
            font=("Arial", 12, "bold"),
            width=150
        )
        date_label.pack(side="left", padx=10)

        # Status text
        status_label = customtkinter.CTkLabel(
            master=item_frame,
            text=status,
            font=("Arial", 12),
            width=120
        )
        status_label.pack(side="left", padx=10)

        # Size label
        size_label = customtkinter.CTkLabel(
            master=item_frame,
            text=size,
            font=("Arial", 12),
            width=80
        )
        size_label.pack(side="left", padx=10)

        # View details button
        view_button = customtkinter.CTkButton(
            master=item_frame,
            text="View Details",
            width=100,
            command=lambda: show_details(date, status, size, description)
        )
        view_button.pack(side="right", padx=10)

        return item_frame

    # Function to show snapshot details
    def show_details(date, status, size, description):
        details_text = f"Date: {date}\nStatus: {status}\nSize: {size}\n\nDescription: {description}"
        details_content.configure(text=details_text)
        rollback_button.configure(state="normal")

        # Store the currently selected snapshot data for rollback
        global selected_snapshot
        selected_snapshot = {
            "date": date,
            "status": status,
            "size": size,
            "description": description
        }

    # Function to perform rollback
    def perform_rollback():
        if 'selected_snapshot' in globals():
            # In a real application, this would trigger the actual rollback process
            confirmation = customtkinter.CTkInputDialog(
                text=f"Are you sure you want to roll back to snapshot from {selected_snapshot['date']}?\n\nType 'CONFIRM' to proceed:",
                title="Confirm Rollback"
            )
            result = confirmation.get_input()

            if result == "CONFIRM":
                progress = show_progress_window(tab_timeline)
                tab_timeline.after(3000, lambda: complete_rollback(progress))

    # Function to show progress window during rollback
    def show_progress_window(parent):
        progress_window = customtkinter.CTkToplevel(parent)
        progress_window.title("Rollback in Progress")
        progress_window.geometry("400x150")
        progress_window.attributes('-topmost', True)

        # Center the window
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        progress_window.geometry(f"400x150+{x}+{y}")

        progress_label = customtkinter.CTkLabel(
            master=progress_window,
            text="Rolling back to selected snapshot...",
            font=("Arial", 14)
        )
        progress_label.pack(pady=20)

        progress_bar = customtkinter.CTkProgressBar(master=progress_window)
        progress_bar.pack(fill="x", padx=20, pady=10)
        progress_bar.set(0)

        # Start progress animation
        def update_progress(value=0):
            if value <= 1.0:
                progress_bar.set(value)
                progress_window.after(100, lambda: update_progress(value + 0.05))

        update_progress()
        return progress_window

    # Function to complete rollback process
    def complete_rollback(progress_window):
        progress_window.destroy()
        success_window = customtkinter.CTkToplevel(tab_timeline)
        success_window.title("Rollback Complete")
        success_window.geometry("400x150")
        success_window.attributes('-topmost', True)

        # Center the window
        screen_width = tab_timeline.winfo_screenwidth()
        screen_height = tab_timeline.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        success_window.geometry(f"400x150+{x}+{y}")

        success_label = customtkinter.CTkLabel(
            master=success_window,
            text="Rollback completed successfully!",
            font=("Arial", 16, "bold")
        )
        success_label.pack(pady=20)

        ok_button = customtkinter.CTkButton(
            master=success_window,
            text="OK",
            command=success_window.destroy
        )
        ok_button.pack(pady=10)

        # Clear the details and refresh the timeline
        details_content.configure(text="Select a snapshot to view details")
        rollback_button.configure(state="disabled")
        refresh_snapshots(machine_var.get())

    # Function to save settings
    def save_settings():
        # In a real application, this would save settings to a configuration file
        confirm_window = customtkinter.CTkToplevel(tab_settings)
        confirm_window.title("Settings Saved")
        confirm_window.geometry("300x100")
        confirm_window.attributes('-topmost', True)

        # Center the window
        screen_width = tab_settings.winfo_screenwidth()
        screen_height = tab_settings.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 100) // 2
        confirm_window.geometry(f"300x100+{x}+{y}")

        confirm_label = customtkinter.CTkLabel(
            master=confirm_window,
            text="Settings saved successfully!",
            font=("Arial", 14)
        )
        confirm_label.pack(pady=20)

        confirm_window.after(2000, confirm_window.destroy)

    # Function to refresh snapshot list
    def refresh_snapshots(machine_name):
        # Clear existing items
        for widget in timeline_frame.winfo_children():
            widget.destroy()

        # Create header
        header_frame = customtkinter.CTkFrame(timeline_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)

        customtkinter.CTkLabel(
            master=header_frame,
            text="",
            width=15
        ).pack(side="left", padx=10)

        customtkinter.CTkLabel(
            master=header_frame,
            text="Date & Time",
            font=("Arial", 12, "bold"),
            width=150
        ).pack(side="left", padx=10)

        customtkinter.CTkLabel(
            master=header_frame,
            text="Status",
            font=("Arial", 12, "bold"),
            width=120
        ).pack(side="left", padx=10)

        customtkinter.CTkLabel(
            master=header_frame,
            text="Size",
            font=("Arial", 12, "bold"),
            width=80
        ).pack(side="left", padx=10)

        if machine_name == "No clients available":
            # Display a message when no clients are available
            no_client_label = customtkinter.CTkLabel(
                master=timeline_frame,
                text="No client machines available. Add clients in User Management.",
                font=("Arial", 14)
            )
            no_client_label.pack(pady=20)
            return

        # In a real application, these would be loaded from a database
        # Generate some sample data for demonstration
        base_date = datetime.now()
        statuses = ["Clean", "Clean", "Clean", "Potential Threat", "Clean", "Corrupted", "Clean"]
        sizes = ["2.4 GB", "2.3 GB", "2.5 GB", "2.4 GB", "2.6 GB", "1.8 GB", "2.5 GB"]
        descriptions = [
            f"Regular system snapshot of {machine_name} - All systems normal",
            f"Regular system snapshot of {machine_name} - All systems normal",
            f"Regular system snapshot of {machine_name} - All systems normal",
            f"Potential threat detected in {machine_name}/system32/drivers - Quarantined",
            f"Regular system snapshot of {machine_name} after threat removal",
            f"File system corruption detected in {machine_name} user profile",
            f"Regular system snapshot of {machine_name} after system repair"
        ]

        for i in range(7):
            date_str = (base_date - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
            create_snapshot_item(
                timeline_frame,
                date_str,
                statuses[i],
                sizes[i],
                descriptions[i]
            )

    # Load initial snapshots
    refresh_snapshots(machines[0] if machines else "No clients available")