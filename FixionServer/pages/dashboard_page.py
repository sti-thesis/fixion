import customtkinter
import tkinter
import os
import sys
from PIL import Image

# Import pages - each in a separate file
from clientmachine_page import open_clientmachine_page
from threatlogs_page import open_threatlogs_page
from analytics_page import open_analytics_page
from snapshot_page import open_snapshot_page
from cloud_page import open_cloud_page
from userm_page import open_userm_page
from systems_page import open_systems_page

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))


# Function to find the assets directory
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


def center_window(window, width, height):
    """Centers a tkinter window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def clear_frame(frame):
    """Clear all widgets from a frame"""
    for widget in frame.winfo_children():
        widget.destroy()


def open_dashboard_content(parent_frame):
    """
    Dashboard main content page
    """
    # Clear the frame first
    clear_frame(parent_frame)

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Dashboard Overview",
        font=("Arial", 24, "bold")
    )
    title.pack(padx=18, pady=20, anchor="w")



def open_dashboard_page(user_info=None):
    """
    Opens the main dashboard window with the dashboard as the default page

    Args:
        user_info (dict): User information dictionary containing username, role, etc.
    """
    dashboard = customtkinter.CTk()
    dashboard.title('Server UI Dashboard')

    # Set dimensions and center the window
    width, height = 1300, 950
    center_window(dashboard, width, height)

    # Create the main layout frames
    sidebar_frame = customtkinter.CTkFrame(master=dashboard, width=250, corner_radius=0)
    sidebar_frame.pack(side="left", fill="y")

    # Main content area
    main_content = customtkinter.CTkFrame(master=dashboard)
    main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Create sidebar items with their corresponding page functions and icons - updated icon filenames
    sidebar_items = [
        {"name": "Dashboard", "page": open_dashboard_content, "icon": "dashboard_icon.png"},
        {"name": "Client machine", "page": open_clientmachine_page, "icon": "client_machine_icon.png"},
        {"name": "Threat logs", "page": open_threatlogs_page, "icon": "threat_logs_icon.png"},
        {"name": "Analytics", "page": open_analytics_page, "icon": "analytics_icon.png"},
        {"name": "Snapshots & Rollbacks", "page": open_snapshot_page, "icon": "snapshot_icon.png"},
        {"name": "Cloud Backups", "page": open_cloud_page, "icon": "cloud_icon.png"},
        {"name": "User Management", "page": open_userm_page, "icon": "userm_icon.png"},
        {"name": "System Settings", "page": open_systems_page, "icon": "systems_icon.png"}
    ]

    # Add logo at the top of sidebar
    try:
        logo_path = os.path.join(assets_path, "icon", "logo.png")
        print(f"Trying to load logo from: {logo_path}")
        logo_image = customtkinter.CTkImage(
            light_image=Image.open(logo_path),
            dark_image=Image.open(logo_path),
            size=(100, 100)
        )

        logo_label = customtkinter.CTkLabel(
            master=sidebar_frame,
            image=logo_image,
            text=""
        )
        logo_label.pack(padx=40, pady=30)
    except Exception as e:
        print(f"Failed to load logo {logo_path}: {e}")
        # Fallback to empty frame as placeholder
        logo_frame = customtkinter.CTkFrame(master=sidebar_frame, width=100, height=100)
        logo_frame.pack(padx=40, pady=20)

    # Add sidebar navigation buttons with vertical layout (icon above text)
    for item in sidebar_items:
        # Create a frame for the button (vertical layout)
        item_frame = customtkinter.CTkFrame(master=sidebar_frame, fg_color="transparent")
        item_frame.pack(fill="x", padx=15, pady=4)  # Increased padding for better spacing

        # Load icon image
        icon_path = os.path.join(assets_path, "icon", item["icon"])

        try:
            # Print path for debugging
            print(f"Trying to load icon from: {icon_path}")

            # Create CTkImage using the icon - LARGER SIZE (45x45)
            icon_image = customtkinter.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(45, 45)  # Increased from 30x30 to 45x45
            )

            # Create a label with the icon image
            icon_label = customtkinter.CTkLabel(
                master=item_frame,
                image=icon_image,
                text=""  # No text, just the icon
            )
            # Pack the icon at the top
            icon_label.pack(pady=(5, 2))

            # Store reference to bind click event later
            icon_element = icon_label
        except Exception as e:
            # If icon not found, create empty frame as placeholder
            print(f"Failed to load icon {icon_path}: {e}")
            icon_frame = customtkinter.CTkFrame(master=item_frame, width=45, height=45)
            icon_frame.pack(pady=(5, 2))
            icon_element = icon_frame

        # Label for the item text - centered below the icon
        item_label = customtkinter.CTkLabel(
            master=item_frame,
            text=item["name"],
            font=("Arial", 12),
            anchor="center"  # Center the text
        )
        item_label.pack(pady=(5, 5))

        # Create function to handle navigation with the correct page
        def create_click_handler(page_func):
            return lambda e: page_func(main_content)

        # Bind click event to navigate to the corresponding page
        item_frame.bind("<Button-1>", create_click_handler(item["page"]))
        icon_element.bind("<Button-1>", create_click_handler(item["page"]))
        item_label.bind("<Button-1>", create_click_handler(item["page"]))

    # Open dashboard content by default
    open_dashboard_content(main_content)

    if user_info:
        dashboard.title(f'Server UI Dashboard - Logged in as {user_info["username"]}')

    dashboard.mainloop()


if __name__ == "__main__":
    # For testing purposes
    open_dashboard_page({"username": "admin", "role": "admin"})