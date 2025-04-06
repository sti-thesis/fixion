import customtkinter
import tkinter


def open_dashboard_window(user_info=None):
    dashboard = customtkinter.CTk()
    dashboard.geometry("900x600")
    dashboard.title('Server UI Dashboard')

    sidebar_frame = customtkinter.CTkFrame(master=dashboard, width=120, corner_radius=0)
    sidebar_frame.pack(side="left", fill="y")

    main_content = customtkinter.CTkFrame(master=dashboard)
    main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    sidebar_items = [
        {"name": "Client machine", "file": "client_machine_page"},
        {"name": "Threat logs", "file": "threat_logs_page"},
        {"name": "Analytics", "file": "analytics_page"},
        {"name": "Snapshots & Rollbacks", "file": "snapshots_page"},
        {"name": "Cloud Backups", "file": "cloud_backups_page"},
        {"name": "User Management", "file": "user_management_page"},
        {"name": "System Settings", "file": "system_settings_page"}
    ]


    logo_frame = customtkinter.CTkFrame(master=sidebar_frame, width=60, height=60)
    logo_frame.pack(padx=30, pady=20)


    for item in sidebar_items:
        item_frame = customtkinter.CTkFrame(master=sidebar_frame, fg_color="transparent")
        item_frame.pack(fill="x", padx=10, pady=10)

        # Icon placeholder
        icon_frame = customtkinter.CTkFrame(master=item_frame, width=30, height=30)
        icon_frame.pack(padx=10, pady=5)

        item_label = customtkinter.CTkLabel(master=item_frame,text=item["name"],anchor="center")
        item_label.pack(pady=2)

        item_frame.bind("<Button-1>", lambda e, file=item["file"]: print(f"Navigating to {file}.py"))

    if user_info:
        dashboard.title(f'Server UI Dashboard - Logged in as {user_info["username"]}')

    dashboard.mainloop()


if __name__ == "__main__":
    open_dashboard_window({"username": "admin", "role": "admin"})