import customtkinter
import tkinter
import tkinter as tk
import os
import sys
import random
import json
from datetime import datetime, timedelta
from PIL import Image
from docutils.nodes import sidebar

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


# DASHBOARD HELPER FUNCTIONS
def load_users():
    """Load users from the JSON file"""
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_client_machines():
    """Extract client machines from users data"""
    users = load_users()
    return [user for user in users if user.get("role") == "client machine"]


def create_stats_card(parent, title, value, icon_name, row, column):
    """Create a single statistics card"""
    card = customtkinter.CTkFrame(parent, corner_radius=10, fg_color="#22232e")
    card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    # Try to load icon
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "assets", "icon", icon_name)

        icon_image = customtkinter.CTkImage(
            light_image=Image.open(icon_path),
            dark_image=Image.open(icon_path),
            size=(32, 32)
        )

        icon_label = customtkinter.CTkLabel(card, image=icon_image, text="")
        icon_label.pack(anchor="w", padx=15, pady=(15, 5))
    except Exception:
        pass

    # Card content
    customtkinter.CTkLabel(card, text=title, font=("Roboto", 14), text_color="#e9e8e8").pack(anchor="w", padx=15,
                                                                                             pady=5)
    customtkinter.CTkLabel(card, text=value, font=("Roboto", 24, "bold"), text_color="#e9e8e8").pack(anchor="w",
                                                                                                     padx=15,
                                                                                                     pady=(5, 15))


def create_professional_pie_chart(canvas, threat_types, total_threats):
    """Create a highly professional, clean pie chart with modern styling"""
    canvas.delete("all")

    # Get canvas dimensions
    canvas.update_idletasks()
    width = canvas.winfo_width() or 300
    height = canvas.winfo_height() or 300

    # Calculate center and radius
    center_x = width // 2
    center_y = height // 2
    base_radius = min(width, height) // 3
    radius = max(base_radius, 80)

    # Professional color palette with accessibility in mind
    professional_colors = [
        "#3B82F6",  # Blue - Primary
        "#10B981",  # Emerald - Success
        "#F59E0B",  # Amber - Warning
        "#EF4444",  # Red - Danger
        "#8B5CF6",  # Violet - Secondary
        "#6B7280",  # Gray - Neutral
        "#EC4899",  # Pink - Accent
        "#14B8A6"  # Teal - Info
    ]

    if total_threats == 0:
        # Professional empty state
        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill="#F8FAFC", outline="#E2E8F0", width=2
        )
        canvas.create_text(
            center_x, center_y,
            text="No Data Available",
            fill="#64748B",
            font=("Roboto", 12),
            anchor="center"
        )
        return

    # Sort threats by count for better visual hierarchy
    sorted_threats = sorted(threat_types.items(), key=lambda x: x[1]["count"], reverse=True)

    start_angle = -90  # Start from top (12 o'clock)

    # Draw subtle drop shadow
    shadow_offset = 2
    shadow_radius = radius + 1
    for i, (threat_type, data) in enumerate(sorted_threats):
        angle_extent = (data["count"] / total_threats) * 360
        canvas.create_arc(
            center_x - shadow_radius + shadow_offset,
            center_y - shadow_radius + shadow_offset,
            center_x + shadow_radius + shadow_offset,
            center_y + shadow_radius + shadow_offset,
            start=start_angle, extent=angle_extent,
            fill="#1F2937", outline="", width=0, style="pieslice",
            stipple="gray25"
        )
        start_angle += angle_extent

    # Reset angle for main chart
    start_angle = -90

    # Draw main pie slices
    for i, (threat_type, data) in enumerate(sorted_threats):
        angle_extent = (data["count"] / total_threats) * 360
        color = professional_colors[i % len(professional_colors)]

        # Main slice
        canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=angle_extent,
            fill=color,
            outline="#FFFFFF",
            width=2,
            style="pieslice"
        )

        start_angle += angle_extent

    # Create modern donut hole
    inner_radius = radius * 0.45

    # Outer ring of donut hole
    canvas.create_oval(
        center_x - inner_radius, center_y - inner_radius,
        center_x + inner_radius, center_y + inner_radius,
        fill="#FFFFFF", outline="#E5E7EB", width=1
    )

    # Inner shadow effect
    inner_shadow_radius = inner_radius - 3
    canvas.create_oval(
        center_x - inner_shadow_radius, center_y - inner_shadow_radius,
        center_x + inner_shadow_radius, center_y + inner_shadow_radius,
        fill="", outline="#F3F4F6", width=1
    )

    # Center text with professional typography
    canvas.create_text(
        center_x, center_y - 8,
        text="Total Threats",
        fill="#6B7280",
        font=("Roboto", 9),
        anchor="center"
    )

    canvas.create_text(
        center_x, center_y + 6,
        text=f"{total_threats:,}",
        fill="#1F2937",
        font=("Roboto", 14, "bold"),
        anchor="center"
    )


def create_compact_legend(parent, threat_types, total_threats):
    """Create a compact legend for the dashboard"""
    # Clear previous legend
    for widget in parent.winfo_children():
        widget.destroy()

    # Professional color palette matching pie chart
    professional_colors = [
        "#3B82F6",  # Blue
        "#10B981",  # Emerald
        "#F59E0B",  # Amber
        "#EF4444",  # Red
        "#8B5CF6",  # Violet
        "#6B7280",  # Gray
        "#EC4899",  # Pink
        "#14B8A6"  # Teal
    ]

    if total_threats == 0:
        empty_label = customtkinter.CTkLabel(
            parent,
            text="No threat data available",
            font=("Roboto", 12),
            text_color="#6B7280"
        )
        empty_label.pack(pady=20)
        return

    # Sort threats for consistency with pie chart
    sorted_threats = sorted(threat_types.items(), key=lambda x: x[1]["count"], reverse=True)

    # Create compact legend entries
    for i, (threat_type, data) in enumerate(sorted_threats):
        percentage = (data["count"] / total_threats) * 100

        # Compact row container
        row_frame = customtkinter.CTkFrame(
            parent,
            fg_color="transparent",
            height=30
        )
        row_frame.pack(fill="x", pady=2, padx=10)

        # Color indicator
        color_frame = customtkinter.CTkFrame(
            row_frame,
            width=12,
            height=12,
            corner_radius=2,
            fg_color=professional_colors[i % len(professional_colors)]
        )
        color_frame.pack(side="left", padx=(0, 8), pady=9)

        # Threat type name
        name_label = customtkinter.CTkLabel(
            row_frame,
            text=threat_type,
            font=("Roboto", 11),
            text_color="#FFFFFF"
        )
        name_label.pack(side="left")

        # Percentage
        percentage_label = customtkinter.CTkLabel(
            row_frame,
            text=f"{percentage:.1f}%",
            font=("Roboto", 11),
            text_color="#94A3B8"
        )
        percentage_label.pack(side="right", padx=(0, 5))


def create_recent_activity_widget(parent):
    """Create a recent activity widget for the dashboard"""
    activity_frame = customtkinter.CTkFrame(parent, fg_color="#22232e", corner_radius=10)
    activity_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Header
    header_label = customtkinter.CTkLabel(
        activity_frame,
        text="Recent Activity",
        font=("Roboto", 16, "bold"),
        text_color="#e9e8e8"
    )
    header_label.pack(anchor="w", padx=20, pady=(15, 10))

    # Sample activities
    activities = [
        {"time": "2 min ago", "action": "Threat blocked", "details": "Malware detected on Client-001",
         "type": "threat"},
        {"time": "15 min ago", "action": "System scan", "details": "Full scan completed on Client-002", "type": "scan"},
        {"time": "1 hour ago", "action": "Client connected", "details": "Client-003 came online", "type": "connection"},
        {"time": "2 hours ago", "action": "Update installed", "details": "Security definitions updated",
         "type": "update"},
    ]

    for activity in activities:
        activity_row = customtkinter.CTkFrame(activity_frame, fg_color="transparent")
        activity_row.pack(fill="x", padx=20, pady=5)

        # Status indicator
        if activity["type"] == "threat":
            indicator_color = "#EF4444"
        elif activity["type"] == "scan":
            indicator_color = "#10B981"
        elif activity["type"] == "connection":
            indicator_color = "#3B82F6"
        else:
            indicator_color = "#F59E0B"

        indicator = customtkinter.CTkFrame(
            activity_row,
            width=8,
            height=8,
            corner_radius=4,
            fg_color=indicator_color
        )
        indicator.pack(side="left", padx=(0, 12), pady=8)

        # Activity details
        details_frame = customtkinter.CTkFrame(activity_row, fg_color="transparent")
        details_frame.pack(side="left", fill="x", expand=True)

        action_label = customtkinter.CTkLabel(
            details_frame,
            text=activity["action"],
            font=("Roboto", 12, "bold"),
            text_color="#e9e8e8"
        )
        action_label.pack(anchor="w")

        detail_label = customtkinter.CTkLabel(
            details_frame,
            text=activity["details"],
            font=("Roboto", 10),
            text_color="#94A3B8"
        )
        detail_label.pack(anchor="w")

        # Time
        time_label = customtkinter.CTkLabel(
            activity_row,
            text=activity["time"],
            font=("Roboto", 10),
            text_color="#6B7280"
        )
        time_label.pack(side="right", padx=(0, 5), pady=8)


def open_dashboard_content(parent_frame):
    """Updated dashboard content with overview elements"""
    clear_frame(parent_frame)

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Dashboard Overview",
        font=("Roboto", 24, "bold"),
        text_color="#e9e8e8"
    )


    # Main scrollable content
    main_content = customtkinter.CTkScrollableFrame(parent_frame, width=950, height=700, fg_color="#22222f")
    main_content.pack(fill="both", expand=True, padx=20, pady=10)

    # ======= STATISTICS CARDS =======
    stats_section = customtkinter.CTkFrame(main_content, fg_color="#22232e")
    stats_section.pack(fill="x", padx=10, pady=10)

    # Configure grid for equal column distribution
    for i in range(4):
        stats_section.grid_columnconfigure(i, weight=1)

    # Create stats cards with dashboard-relevant data
    stats_data = [
        ("Total Threats", str(random.randint(120, 300)), "threat_logs_icon.png"),
        ("Active Clients", str(len(get_client_machines())), "client_machine_icon.png"),
        ("System Status", "Healthy", "systems_icon.png"),
        ("Last Scan", "2 hrs ago", "analytics_icon.png")
    ]

    for i, (title, value, icon) in enumerate(stats_data):
        create_stats_card(stats_section, title, value, icon, 0, i)

    # ======= MAIN DASHBOARD CONTENT =======
    dashboard_content = customtkinter.CTkFrame(main_content, fg_color="transparent")
    dashboard_content.pack(fill="x", padx=10, pady=10)

    # Left side - Threat Analysis
    left_side = customtkinter.CTkFrame(dashboard_content, fg_color="#22232e", corner_radius=10)
    left_side.pack(side="left", fill="both", expand=True, padx=(0, 5))

    # Threat analysis header
    threat_header = customtkinter.CTkLabel(
        left_side,
        text="Threat Distribution",
        font=("Roboto", 16, "bold"),
        text_color="#e9e8e8"
    )
    threat_header.pack(anchor="w", padx=20, pady=(15, 10))

    # Container for pie chart and legend
    chart_container = customtkinter.CTkFrame(left_side, fg_color="transparent")
    chart_container.pack(fill="both", expand=True, padx=20, pady=15)

    # Pie chart section
    pie_chart_section = customtkinter.CTkFrame(chart_container, fg_color="#1c253a", corner_radius=12)
    pie_chart_section.pack(side="left", fill="both", expand=True, padx=(0, 10))

    pie_canvas = tk.Canvas(pie_chart_section, bg="#1c253a", highlightthickness=0, height=250, width=250)
    pie_canvas.pack(fill="both", expand=True, padx=15, pady=15)

    # Bind resize event to redraw chart
    def on_canvas_configure(event):
        # Redraw chart when canvas size changes
        pie_canvas.after(50, lambda: create_professional_pie_chart(pie_canvas, threat_types, total_threats))

    pie_canvas.bind("<Configure>", on_canvas_configure)


    # Legend section
    legend_section = customtkinter.CTkFrame(chart_container, fg_color="#1c253a", corner_radius=12)
    legend_section.pack(side="right", fill="y", padx=(10, 0))

    # Generate threat type data
    threat_types = {
        "Malware": {"count": random.randint(45, 65)},
        "Phishing": {"count": random.randint(25, 35)},
        "Ransomware": {"count": random.randint(8, 15)},
        "Trojan": {"count": random.randint(15, 25)},
        "Spyware": {"count": random.randint(10, 18)},
        "Zero-day": {"count": random.randint(3, 8)}
    }

    total_threats = sum(threat["count"] for threat in threat_types.values())

    # Draw pie chart and create legend
    pie_canvas.after(100, lambda: create_professional_pie_chart(pie_canvas, threat_types, total_threats))
    create_compact_legend(legend_section, threat_types, total_threats)

    # Right side - Recent Activity
    right_side = customtkinter.CTkFrame(dashboard_content, fg_color="transparent")
    right_side.pack(side="right", fill="both", expand=True, padx=(5, 0))

    create_recent_activity_widget(right_side)

    # ======= SYSTEM HEALTH OVERVIEW =======
    health_section = customtkinter.CTkFrame(main_content, fg_color="#22232e")
    health_section.pack(fill="x", padx=10, pady=10)

    health_header = customtkinter.CTkLabel(
        health_section,
        text="System Health Overview",
        font=("Roboto", 16, "bold"),
        text_color="#e9e8e8"
    )
    health_header.pack(anchor="w", padx=20, pady=(15, 10))

    # Health metrics container
    health_metrics = customtkinter.CTkFrame(health_section, fg_color="transparent")
    health_metrics.pack(fill="x", padx=20, pady=(0, 20))

    # Create health metric cards
    health_data = [
        ("CPU Usage", f"{random.randint(15, 45)}%", "#10B981"),
        ("Memory Usage", f"{random.randint(30, 70)}%", "#F59E0B"),
        ("Disk Usage", f"{random.randint(20, 60)}%", "#3B82F6"),
        ("Network Status", "Optimal", "#10B981")
    ]

    for i, (metric, value, color) in enumerate(health_data):
        metric_card = customtkinter.CTkFrame(health_metrics, fg_color="#1c253a", corner_radius=8)
        metric_card.pack(side="left", fill="x", expand=True, padx=5, pady=10)

        # Metric header
        metric_label = customtkinter.CTkLabel(
            metric_card,
            text=metric,
            font=("Roboto", 12),
            text_color="#94A3B8"
        )
        metric_label.pack(pady=(15, 5))

        # Metric value
        value_label = customtkinter.CTkLabel(
            metric_card,
            text=value,
            font=("Roboto", 18, "bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 15))

    # ======= QUICK ACTIONS =======
    actions_section = customtkinter.CTkFrame(main_content, fg_color="#22232e")
    actions_section.pack(fill="x", padx=10, pady=10)

    actions_header = customtkinter.CTkLabel(
        actions_section,
        text="Quick Actions",
        font=("Roboto", 16, "bold"),
        text_color="#e9e8e8"
    )
    actions_header.pack(anchor="w", padx=20, pady=(15, 10))

    # Actions container
    actions_container = customtkinter.CTkFrame(actions_section, fg_color="transparent")
    actions_container.pack(fill="x", padx=20, pady=(0, 20))

    # Action buttons
    actions = [
        ("Full System Scan", "#3B82F6"),
        ("Update Definitions", "#10B981"),
        ("View Threat Logs", "#F59E0B"),
        ("Generate Report", "#8B5CF6")
    ]

    for action, color in actions:
        action_btn = customtkinter.CTkButton(
            actions_container,
            text=action,
            font=("Roboto", 12),
            fg_color=color,
            hover_color=color,
            width=200,
            height=35
        )
        action_btn.pack(side="left", fill="x", expand=True, padx=5)


def open_dashboard_page(user_info=None):
    """
    Opens the main dashboard window with the dashboard as the default page

    Args:
        user_info (dict): User information dictionary containing username, role, etc.
    """
    mainframe = customtkinter.CTk(fg_color="#15141b")
    mainframe.title('Server UI Dashboard')

    # Set dimensions and center the window

    width, height = 1100, 750
    center_window(dashboard, width, height)


    # Create the main layout frames
    sidebar_frame = customtkinter.CTkFrame(master=mainframe, width=118, corner_radius=24, fg_color="#122a3e")
    sidebar_frame.pack(side="left", fill="y")

    sidebarinv_frame = customtkinter.CTkFrame(
        sidebar_frame,
        fg_color="#122a3e",
        width=20,
        height=800,  # Match your window height
        corner_radius=0
    )
    sidebarinv_frame.place(x=0, y=0)  # Position at the very left

    # Ensure the sidebar_frame maintains its width
    sidebar_frame.pack_propagate(False)

    # Main content area
    main_content = customtkinter.CTkFrame(master=mainframe, fg_color="#15141b", border_width=0)
    main_content.pack(side="right", fill="both", expand=True)

    # Create sidebar items with their corresponding page functions and icons - updated icon filenames
    sidebar_items = [
        {"name": "Dashboard", "page": open_dashboard_content, "icon": "dashboard_icon.png"},
        {"name": "Client machine", "page": open_clientmachine_page, "icon": "client_machine_icon.png"},
        {"name": "Threat logs", "page": open_threatlogs_page, "icon": "threat_logs_icon.png"},
        {"name": "Analytics", "page": open_analytics_page, "icon": "analytics_icon.png"},
        {"name": "Snapshots", "page": open_snapshot_page, "icon": "snapshot_icon.png"},
        {"name": "User Management", "page": open_userm_page, "icon": "userm_icon.png"},
        {"name": "System Settings", "page": open_systems_page, "icon": "systems_icon.png"}
    ]

    logo_path = os.path.join(os.path.dirname(__file__), "logo", "fixion_logo.png")
    print(f"Trying to load logo from: {logo_path}")
    logo_image = customtkinter.CTkImage(

        light_image=Image.open(logo_path),
        size=(38, 48)
    )


    logo_label = customtkinter.CTkLabel(
        master=sidebar_frame,
        image=logo_image,
        text=""
    )
    logo_label.pack(padx=8, pady=13)

    # Add sidebar navigation buttons with vertical layout (icon above text)
    for item in sidebar_items:
        # Create a frame for the button (vertical layout)
        item_frame = customtkinter.CTkFrame(master=sidebar_frame, fg_color="transparent")
        item_frame.pack(fill="x", padx=2, pady=4)  # Increased padding for better spacing

        # Load icon image
        icon_path = os.path.join(assets_path, "icon", item["icon"])

        try:
            # Print path for debugging
            print(f"Trying to load icon from: {icon_path}")

            # Create CTkImage using the icon - LARGER SIZE (45x45)
            icon_image = customtkinter.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),

                size=(25, 25)  # Increased from 30x30 to 45x45

            )

            # Create a label with the icon image
            icon_label = customtkinter.CTkLabel(
                master=item_frame,
                image=icon_image,
                text=""  # No text, just the icon
            )
            # Pack the icon at the top

            icon_label.pack(pady=(5, 10))


            # Store reference to bind click event later
            icon_element = icon_label
        except Exception as e:
            # If icon not found, create empty frame as placeholder
            print(f"Failed to load icon {icon_path}: {e}")
            icon_frame = customtkinter.CTkFrame(master=item_frame, width=35, height=35)
            icon_frame.pack(pady=(1, 1))
            icon_element = icon_frame

        # Label for the item text - centered below the icon
        item_label = customtkinter.CTkLabel(
            master=item_frame,
            text=item["name"],

            font=("Arial", 11),

            anchor="center"  # Center the text
        )
        item_label.pack(pady=(5, 10))

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
        mainframe.title(f'Server UI Dashboard - Logged in as {user_info["username"]}')

    mainframe.mainloop()


if __name__ == "__main__":
    # For testing purposes
    open_dashboard_page({"username": "admin", "role": "admin"})