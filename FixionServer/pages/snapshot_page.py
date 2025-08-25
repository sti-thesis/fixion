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
        text_color="#e9e8e8"
    )
    title.pack(anchor="w", padx=12, pady=12)

    # Create tabs for different sections
    tab_view = customtkinter.CTkTabview(
        master=parent_frame,
        fg_color="#22222f",
        segmented_button_fg_color="#22232e",
        segmented_button_selected_color="#323b50",
        segmented_button_unselected_color="#22232e",
        text_color="#e9e8e8"
    )
    tab_view.pack(fill="both", expand=True, padx=20, pady=10)

    tab_timeline = tab_view.add("Snapshot Timeline")
    tab_settings = tab_view.add("Settings")

    # === Timeline Tab ===
    # Control frame for refresh button
    control_frame = customtkinter.CTkFrame(tab_timeline, fg_color="#22232e")
    control_frame.pack(fill="x", padx=10, pady=10)

    control_title = customtkinter.CTkLabel(
        master=control_frame,
        text="System Snapshots - All Client Machines",
        font=("Roboto", 16, "bold"),
        text_color="#e9e8e8"
    )
    control_title.pack(side="left", padx=15, pady=15)

    refresh_button = customtkinter.CTkButton(
        master=control_frame,
        text="Refresh",
        width=100,
        command=lambda: refresh_snapshots(),
        fg_color="#586b78",
        hover_color="#6d7f8c",
        text_color="#e9e8e8",
        font=("Roboto", 12)
    )
    refresh_button.pack(side="right", padx=15, pady=15)

    # Load machines from users.json file
    def load_client_machines():
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
                # Filter only client machines
                clients = [user for user in users if user.get('role') == 'client machine']
                return clients
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Timeline frame with scrollable content
    timeline_frame = customtkinter.CTkScrollableFrame(
        tab_timeline,
        fg_color="#22232e",
        scrollbar_fg_color="#22232e",
        scrollbar_button_color="#586b78",
        scrollbar_button_hover_color="#6d7f8c"
    )
    timeline_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Details frame at the bottom
    details_frame = customtkinter.CTkFrame(tab_timeline, fg_color="#22232e")
    details_frame.pack(fill="x", padx=10, pady=10)

    details_title = customtkinter.CTkLabel(
        master=details_frame,
        text="Snapshot Details",
        font=("Roboto", 16, "bold"),
        text_color="#e9e8e8"
    )
    details_title.pack(anchor="w", padx=15, pady=(15, 5))

    details_content = customtkinter.CTkLabel(
        master=details_frame,
        text="Select a snapshot to view details",
        font=("Roboto", 12),
        text_color="#a9b8c4",
        justify="left",
        anchor="w"
    )
    details_content.pack(anchor="w", padx=15, pady=5, fill="x")

    rollback_button = customtkinter.CTkButton(
        master=details_frame,
        text="Rollback to Selected Snapshot",
        state="disabled",
        command=lambda: perform_rollback(),
        fg_color="#63003d",
        hover_color="#7a0049",
        text_color="#e9e8e8",
        font=("Roboto", 12)
    )
    rollback_button.pack(anchor="e", padx=15, pady=15)

    # === Settings Tab ===
    settings_frame = customtkinter.CTkFrame(tab_settings, fg_color="#22232e")
    settings_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Configure grid weights for better layout
    settings_frame.grid_columnconfigure(0, weight=1)
    settings_frame.grid_columnconfigure(1, weight=1)

    # Snapshot frequency setting
    frequency_label = customtkinter.CTkLabel(
        master=settings_frame,
        text="Snapshot Frequency:",
        font=("Roboto", 14),
        text_color="#e9e8e8"
    )
    frequency_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

    frequency_options = ["Every 12 hours", "Daily", "Every 2 days", "Weekly"]
    frequency_var = tk.StringVar(value=frequency_options[1])

    frequency_menu = customtkinter.CTkOptionMenu(
        master=settings_frame,
        values=frequency_options,
        variable=frequency_var,
        fg_color="#323b50",
        button_color="#323b50",
        button_hover_color="#414a61",
        dropdown_fg_color="#22232e",
        text_color="#e9e8e8",
        dropdown_text_color="#e9e8e8"
    )
    frequency_menu.grid(row=0, column=1, padx=20, pady=15, sticky="w")

    # Retention policy setting
    retention_label = customtkinter.CTkLabel(
        master=settings_frame,
        text="Retention Policy:",
        font=("Roboto", 14),
        text_color="#e9e8e8"
    )
    retention_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")

    retention_options = ["Keep 7 days", "Keep 14 days", "Keep 30 days", "Keep 90 days"]
    retention_var = tk.StringVar(value=retention_options[2])

    retention_menu = customtkinter.CTkOptionMenu(
        master=settings_frame,
        values=retention_options,
        variable=retention_var,
        fg_color="#323b50",
        button_color="#323b50",
        button_hover_color="#414a61",
        dropdown_fg_color="#22232e",
        text_color="#e9e8e8",
        dropdown_text_color="#e9e8e8"
    )
    retention_menu.grid(row=1, column=1, padx=20, pady=15, sticky="w")

    # Auto-snapshot setting
    auto_snapshot = tk.BooleanVar(value=True)
    auto_checkbox = customtkinter.CTkCheckBox(
        master=settings_frame,
        text="Enable automatic snapshots",
        variable=auto_snapshot,
        text_color="#e9e8e8",
        font=("Roboto", 12),
        checkmark_color="#22232e",
        fg_color="#1b720f",
        hover_color="#2a8f1e"
    )
    auto_checkbox.grid(row=2, column=0, columnspan=2, padx=20, pady=15, sticky="w")

    # Pre-rollback snapshot setting
    pre_rollback = tk.BooleanVar(value=True)
    pre_rollback_checkbox = customtkinter.CTkCheckBox(
        master=settings_frame,
        text="Create snapshot before rollback",
        variable=pre_rollback,
        text_color="#e9e8e8",
        font=("Roboto", 12),
        checkmark_color="#22232e",
        fg_color="#1b720f",
        hover_color="#2a8f1e"
    )
    pre_rollback_checkbox.grid(row=3, column=0, columnspan=2, padx=20, pady=15, sticky="w")

    # Save settings button
    save_button = customtkinter.CTkButton(
        master=settings_frame,
        text="Save Settings",
        command=lambda: save_settings(),
        fg_color="#1b720f",
        hover_color="#2a8f1e",
        text_color="#e9e8e8",
        font=("Roboto", 12)
    )
    save_button.grid(row=4, column=1, padx=20, pady=20, sticky="e")

    # Function to create a single snapshot item in the timeline
    def create_snapshot_item(parent, client_name, date, size, status, description):
        # Status colors
        status_colors = {
            "Clean": "#1b720f",  # Green
            "Potential Threat": "#ff9800",  # Orange
            "Corrupted": "#63003d"  # Red
        }

        item_frame = customtkinter.CTkFrame(parent, fg_color="#323b50", corner_radius=8)
        item_frame.pack(fill="x", padx=5, pady=5)

        # Create a container for better layout
        content_frame = customtkinter.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)

        # Status indicator (colored circle)
        status_indicator = customtkinter.CTkFrame(
            master=content_frame,
            width=15,
            height=15,
            corner_radius=10,
            fg_color=status_colors.get(status, "#808080")
        )
        status_indicator.pack(side="left", padx=(0, 15))

        # Client name
        client_display = f"{client_name}"
        if len(client_display) > 25:
            client_display = client_display[:22] + "..."

        client_label = customtkinter.CTkLabel(
            master=content_frame,
            text=client_display,
            font=("Roboto", 12, "bold"),
            text_color="#e9e8e8",
            width=200
        )
        client_label.pack(side="left", padx=(0, 20))

        # Date and time
        date_label = customtkinter.CTkLabel(
            master=content_frame,
            text=date,
            font=("Roboto", 11),
            text_color="#a9b8c4",
            width=160
        )
        date_label.pack(side="left", padx=(0, 20))

        # Size label
        size_label = customtkinter.CTkLabel(
            master=content_frame,
            text=size,
            font=("Roboto", 12),
            text_color="#e9e8e8",
            width=100
        )
        size_label.pack(side="left", padx=(0, 20))

        # View details button
        view_button = customtkinter.CTkButton(
            master=content_frame,
            text="View Details",
            width=120,
            command=lambda: show_details(client_name, date, status, size, description),
            fg_color="#586b78",
            hover_color="#6d7f8c",
            text_color="#e9e8e8",
            font=("Roboto", 11)
        )
        view_button.pack(side="right")

        return item_frame

    # Function to show snapshot details
    def show_details(client_name, date, status, size, description):
        details_text = f"Client: {client_name}\nDate: {date}\nStatus: {status}\nSize: {size}\n\nDescription: {description}"
        details_content.configure(text=details_text)
        rollback_button.configure(state="normal")

        # Store the currently selected snapshot data for rollback
        global selected_snapshot
        selected_snapshot = {
            "client": client_name,
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
                text=f"Are you sure you want to roll back {selected_snapshot['client']} to snapshot from {selected_snapshot['date']}?\n\nType 'CONFIRM' to proceed:",
                title="Confirm Rollback",
                fg_color="#22232e",
                text_color="#e9e8e8"
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
        progress_window.configure(fg_color="#22232e")

        # Center the window
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        progress_window.geometry(f"400x150+{x}+{y}")

        progress_label = customtkinter.CTkLabel(
            master=progress_window,
            text="Rolling back to selected snapshot...",
            font=("Roboto", 14),
            text_color="#e9e8e8"
        )
        progress_label.pack(pady=20)

        progress_bar = customtkinter.CTkProgressBar(
            master=progress_window,
            fg_color="#323b50",
            progress_color="#1b720f"
        )
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
        success_window.configure(fg_color="#22232e")

        # Center the window
        screen_width = tab_timeline.winfo_screenwidth()
        screen_height = tab_timeline.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        success_window.geometry(f"400x150+{x}+{y}")

        success_label = customtkinter.CTkLabel(
            master=success_window,
            text="Rollback completed successfully!",
            font=("Roboto", 16, "bold"),
            text_color="#1b720f"
        )
        success_label.pack(pady=20)

        ok_button = customtkinter.CTkButton(
            master=success_window,
            text="OK",
            command=success_window.destroy,
            fg_color="#1b720f",
            hover_color="#2a8f1e",
            text_color="#e9e8e8"
        )
        ok_button.pack(pady=10)

        # Clear the details and refresh the timeline
        details_content.configure(text="Select a snapshot to view details")
        rollback_button.configure(state="disabled")
        refresh_snapshots()

    # Function to save settings
    def save_settings():
        # In a real application, this would save settings to a configuration file
        confirm_window = customtkinter.CTkToplevel(tab_settings)
        confirm_window.title("Settings Saved")
        confirm_window.geometry("300x100")
        confirm_window.attributes('-topmost', True)
        confirm_window.configure(fg_color="#22232e")

        # Center the window
        screen_width = tab_settings.winfo_screenwidth()
        screen_height = tab_settings.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 100) // 2
        confirm_window.geometry(f"300x100+{x}+{y}")

        confirm_label = customtkinter.CTkLabel(
            master=confirm_window,
            text="Settings saved successfully!",
            font=("Roboto", 14),
            text_color="#1b720f"
        )
        confirm_label.pack(pady=20)

        confirm_window.after(2000, confirm_window.destroy)

    # Function to refresh snapshot list
    def refresh_snapshots():
        # Clear existing items
        for widget in timeline_frame.winfo_children():
            widget.destroy()

        # Create header
        header_frame = customtkinter.CTkFrame(timeline_frame, fg_color="#414a61", corner_radius=8)
        header_frame.pack(fill="x", padx=5, pady=(5, 10))

        header_content = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=10)

        customtkinter.CTkLabel(
            master=header_content,
            text="",
            width=15
        ).pack(side="left", padx=(0, 15))

        customtkinter.CTkLabel(
            master=header_content,
            text="Client Machine",
            font=("Roboto", 12, "bold"),
            text_color="#e9e8e8",
            width=200
        ).pack(side="left", padx=(0, 20))

        customtkinter.CTkLabel(
            master=header_content,
            text="Save Point Date/Time",
            font=("Roboto", 12, "bold"),
            text_color="#e9e8e8",
            width=160
        ).pack(side="left", padx=(0, 20))

        customtkinter.CTkLabel(
            master=header_content,
            text="Size",
            font=("Roboto", 12, "bold"),
            text_color="#e9e8e8",
            width=100
        ).pack(side="left", padx=(0, 20))

        customtkinter.CTkLabel(
            master=header_content,
            text="Actions",
            font=("Roboto", 12, "bold"),
            text_color="#e9e8e8"
        ).pack(side="right")

        # Load client machines
        clients = load_client_machines()

        if not clients:
            # Display a message when no clients are available
            no_client_frame = customtkinter.CTkFrame(timeline_frame, fg_color="#323b50", corner_radius=8)
            no_client_frame.pack(fill="x", padx=5, pady=20)

            no_client_label = customtkinter.CTkLabel(
                master=no_client_frame,
                text="No client machines available. Add clients in User Management.",
                font=("Roboto", 14),
                text_color="#a9b8c4"
            )
            no_client_label.pack(pady=30)
            return

        # Generate snapshots for all clients
        base_date = datetime.now()
        statuses = ["Clean", "Clean", "Clean", "Potential Threat", "Clean", "Corrupted", "Clean"]
        sizes = ["2.4 GB", "2.3 GB", "2.5 GB", "2.4 GB", "2.6 GB", "1.8 GB", "2.5 GB"]

        # Create snapshot entries for each client
        all_snapshots = []

        for client in clients:
            client_name = client.get('username', 'Unknown')

            # Generate 3-5 snapshots per client
            num_snapshots = random.randint(3, 5)
            for i in range(num_snapshots):
                # Random date within last 30 days
                days_back = random.randint(0, 30)
                hours_back = random.randint(0, 23)
                snapshot_date = base_date - timedelta(days=days_back, hours=hours_back)

                status = random.choice(statuses)
                size = random.choice(sizes)
                description = f"System snapshot of {client_name} - {status} state detected"

                all_snapshots.append({
                    'client_name': client_name,
                    'date': snapshot_date,
                    'status': status,
                    'size': size,
                    'description': description
                })

        # Sort snapshots by date (newest first)
        all_snapshots.sort(key=lambda x: x['date'], reverse=True)

        # Create snapshot items
        for snapshot in all_snapshots:
            date_str = snapshot['date'].strftime("%Y-%m-%d %H:%M:%S")
            create_snapshot_item(
                timeline_frame,
                snapshot['client_name'],
                date_str,
                snapshot['size'],
                snapshot['status'],
                snapshot['description']
            )

    # Load initial snapshots
    refresh_snapshots()