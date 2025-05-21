import customtkinter
import tkinter as tk
from tkinter import ttk
import random
import json
import os
from datetime import datetime, timedelta
import math
from PIL import Image


# Mock data generation functions for demonstration
def generate_mock_threat_data(days=30):
    """Generate sample threat detection data for demonstration"""
    today = datetime.now()
    data = []
    threat_types = ["Malware", "Phishing", "Ransomware", "Trojan", "Spyware", "Zero-day"]
    severity_levels = ["Critical", "High", "Medium", "Low"]

    # Generate between 50-150 threats over the time period
    num_threats = random.randint(50, 150)

    for _ in range(num_threats):
        # Random date within the specified days
        random_day = random.randint(0, days - 1)
        date = today - timedelta(days=random_day)

        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "time": date.strftime("%H:%M:%S"),
            "threat_type": random.choice(threat_types),
            "severity": random.choice(severity_levels),
            "client_id": random.randint(1, 5),
            "resolved": random.random() > 0.2  # 80% chance of being resolved
        })

    return data


def generate_mock_system_data(days=30):
    """Generate sample system performance data for demonstration"""
    today = datetime.now()
    data = []

    # Generate data points for each day
    for day in range(days):
        date = today - timedelta(days=day)

        # Generate some fluctuation in system metrics
        cpu_usage = random.uniform(10, 60)
        memory_usage = random.uniform(30, 70)
        scan_time = random.uniform(5, 20)

        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "scan_time": scan_time,
            "active_clients": random.randint(1, 5)
        })

    return data


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


def open_analytics_page(parent_frame):
    """
    Analytics dashboard page with charts and statistics
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Analytics Dashboard",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=20, anchor="w", padx=20)

    # Create a scrollable main content frame
    main_content = customtkinter.CTkScrollableFrame(
        master=parent_frame,
        width=950,
        height=800
    )
    main_content.pack(fill="both", expand=True, padx=20, pady=10)

    # ======= TOP STATS SECTION =======
    stats_frame = customtkinter.CTkFrame(master=main_content)
    stats_frame.pack(fill="x", padx=10, pady=10)

    # Create a grid of stats cards
    grid_frame = customtkinter.CTkFrame(master=stats_frame, fg_color="transparent")
    grid_frame.pack(fill="x", padx=20, pady=20)

    # Define the statistics cards
    stats_cards = [
        {"title": "Total Threats Detected", "value": str(random.randint(120, 300)), "icon": "threat_logs_icon.png"},
        {"title": "Active Clients", "value": str(len(get_client_machines())), "icon": "client_machine_icon.png"},
        {"title": "Resolved Threats", "value": str(random.randint(100, 250)), "icon": "systems_icon.png"},
        {"title": "Critical Alerts", "value": str(random.randint(5, 20)), "icon": "analytics_icon.png"}
    ]

    # Create and place stat cards in a grid
    for i, card in enumerate(stats_cards):
        col = i % 4
        row = i // 4

        # Create a frame for each card
        card_frame = customtkinter.CTkFrame(master=grid_frame, corner_radius=10)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Try to load icon - fallback to text if icon not found
        try:
            # Get assets path - similar to dashboard_page.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "assets", "icon", card["icon"])

            icon_image = customtkinter.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(32, 32)
            )

            icon_label = customtkinter.CTkLabel(
                master=card_frame,
                image=icon_image,
                text=""
            )
            icon_label.pack(anchor="w", padx=15, pady=(15, 5))
        except Exception as e:
            # If icon loading fails, just skip it
            pass

        # Card title
        card_title = customtkinter.CTkLabel(
            master=card_frame,
            text=card["title"],
            font=("Arial", 14)
        )
        card_title.pack(anchor="w", padx=15, pady=5)

        # Card value
        card_value = customtkinter.CTkLabel(
            master=card_frame,
            text=card["value"],
            font=("Arial", 24, "bold")
        )
        card_value.pack(anchor="w", padx=15, pady=(5, 15))

    # Configure grid column widths to be equal
    for i in range(4):
        grid_frame.grid_columnconfigure(i, weight=1)

    # ======= THREAT DETECTION CHART =======
    chart_frame = customtkinter.CTkFrame(master=main_content)
    chart_frame.pack(fill="x", padx=10, pady=10)

    chart_title = customtkinter.CTkLabel(
        master=chart_frame,
        text="Threat Detection Trend (30 Days)",
        font=("Arial", 16, "bold")
    )
    chart_title.pack(anchor="w", padx=20, pady=10)

    # Use a standard ttk.Frame for embedding the chart
    # We'll create a simple bar chart representation for now
    chart_canvas_frame = tk.Frame(master=chart_frame, bg="#1c253a")
    chart_canvas_frame.pack(fill="both", padx=20, pady=10, ipady=150)  # Fixed height

    # Generate mock data for last 30 days
    threat_data = generate_mock_threat_data(30)

    # Count threats by date
    threat_counts = {}
    for threat in threat_data:
        date = threat["date"]
        if date in threat_counts:
            threat_counts[date] += 1
        else:
            threat_counts[date] = 1

    # Sort dates and create chart data
    sorted_dates = sorted(threat_counts.keys())

    # Only use every 5th date for labels to avoid crowding
    chart_dates = [date if i % 5 == 0 else "" for i, date in enumerate(sorted_dates)]
    chart_values = [threat_counts[date] for date in sorted_dates]

    # Calculate max value for scaling
    max_value = max(chart_values) if chart_values else 10

    # Draw simple bar chart using Canvas
    chart_canvas = tk.Canvas(chart_canvas_frame, bg="#1c253a", highlightthickness=0)
    chart_canvas.pack(fill="both", expand=True)

    # Chart dimensions
    chart_width = 900
    chart_height = 150
    bar_spacing = chart_width / (len(chart_values) * 1.5)
    bottom_margin = 30

    # Function to draw the chart
    def draw_chart():
        chart_canvas.delete("all")

        # Draw X and Y axes
        chart_canvas.create_line(40, chart_height - bottom_margin, chart_width - 20,
                                 chart_height - bottom_margin, fill="#a9b8c4", width=2)
        chart_canvas.create_line(40, 20, 40, chart_height - bottom_margin, fill="#a9b8c4", width=2)

        # Draw bars
        for i, value in enumerate(chart_values):
            # Bar height scaled to max value
            bar_height = (value / max_value) * (chart_height - bottom_margin - 30)

            # Bar position
            x1 = 50 + (i * bar_spacing * 1.5)
            y1 = chart_height - bottom_margin - bar_height
            x2 = x1 + bar_spacing
            y2 = chart_height - bottom_margin

            # Draw bar with gradient color based on value
            color = f"#{int(min(255, 100 + (155 * value / max_value))):02x}4080"
            chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            # Add date label every 5th bar
            if chart_dates[i]:
                chart_canvas.create_text(x1 + bar_spacing / 2, chart_height - bottom_margin + 15,
                                         text=chart_dates[i][5:], fill="#a9b8c4", font=("Arial", 8))

        # Add Y-axis labels
        for i in range(5):
            value = int(max_value * i / 4)
            y_pos = chart_height - bottom_margin - (i * (chart_height - bottom_margin - 30) / 4)
            chart_canvas.create_text(30, y_pos, text=str(value), fill="#a9b8c4", font=("Arial", 8))

    draw_chart()

    # Configure resize behavior
    def on_resize(event):
        nonlocal chart_width
        chart_width = event.width - 20
        nonlocal bar_spacing
        bar_spacing = chart_width / (len(chart_values) * 1.5)
        draw_chart()

    chart_canvas.bind("<Configure>", on_resize)

    # ======= CLIENT ACTIVITY SECTION =======
    clients_frame = customtkinter.CTkFrame(master=main_content)
    clients_frame.pack(fill="x", padx=10, pady=10)

    clients_title = customtkinter.CTkLabel(
        master=clients_frame,
        text="Client Machine Activity",
        font=("Arial", 16, "bold")
    )
    clients_title.pack(anchor="w", padx=20, pady=10)

    # Create a table for client activity
    table_frame = customtkinter.CTkFrame(master=clients_frame)
    table_frame.pack(fill="x", padx=20, pady=10)

    # Get actual client machines
    clients = get_client_machines()

    # If no clients found, show a message
    if not clients:
        no_clients_label = customtkinter.CTkLabel(
            master=table_frame,
            text="No client machines found. Add clients in User Management.",
            font=("Arial", 12)
        )
        no_clients_label.pack(pady=20)
    else:
        # Table headers
        header_frame = customtkinter.CTkFrame(master=table_frame, fg_color="#323b50")
        header_frame.pack(fill="x", pady=(0, 2))

        headers = ["Client Name", "Status", "Last Active", "Threats Detected", "Protection Status"]

        for i, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(
                master=header_frame,
                text=header,
                font=("Arial", 12, "bold")
            )
            header_label.grid(row=0, column=i, padx=15, pady=10, sticky="w")
            header_frame.grid_columnconfigure(i, weight=1)

        # Table rows
        for i, client in enumerate(clients):
            row_frame = customtkinter.CTkFrame(master=table_frame)
            row_frame.pack(fill="x", pady=1)

            # Client name
            name_label = customtkinter.CTkLabel(
                master=row_frame,
                text=client.get("username", "Unknown"),
                font=("Arial", 12)
            )
            name_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

            # Status
            status_text = "Online" if client.get("active", True) else "Offline"
            status_color = "#1b720f" if client.get("active", True) else "#63003d"

            status_frame = customtkinter.CTkFrame(master=row_frame, fg_color="transparent")
            status_frame.grid(row=0, column=1, padx=15, pady=10, sticky="w")

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
                text=status_text,
                font=("Arial", 12)
            )
            status_label.pack(side="left")

            # Last active - random recent time
            last_active = datetime.now() - timedelta(
                minutes=0 if client.get("active", True) else random.randint(60, 10080)
            )

            if client.get("active", True):
                last_active_text = "Now"
            elif (datetime.now() - last_active).days > 0:
                last_active_text = f"{(datetime.now() - last_active).days} days ago"
            else:
                last_active_text = f"{int((datetime.now() - last_active).seconds / 3600)} hours ago"

            last_active_label = customtkinter.CTkLabel(
                master=row_frame,
                text=last_active_text,
                font=("Arial", 12)
            )
            last_active_label.grid(row=0, column=2, padx=15, pady=10, sticky="w")

            # Threats detected - random number
            threats = random.randint(0, 20)
            threats_label = customtkinter.CTkLabel(
                master=row_frame,
                text=str(threats),
                font=("Arial", 12)
            )
            threats_label.grid(row=0, column=3, padx=15, pady=10, sticky="w")

            # Protection status
            protection_status = random.choice(["Protected", "Update Required", "Protected"])
            protection_color = "#1b720f" if protection_status == "Protected" else "#714bae"

            protection_label = customtkinter.CTkLabel(
                master=row_frame,
                text=protection_status,
                text_color=protection_color,
                font=("Arial", 12)
            )
            protection_label.grid(row=0, column=4, padx=15, pady=10, sticky="w")

            # Configure equal column widths
            for col in range(5):
                row_frame.grid_columnconfigure(col, weight=1)

    # ======= THREAT BREAKDOWN SECTION =======
    threat_breakdown_frame = customtkinter.CTkFrame(master=main_content)
    threat_breakdown_frame.pack(fill="x", padx=10, pady=10)

    threat_breakdown_title = customtkinter.CTkLabel(
        master=threat_breakdown_frame,
        text="Threat Type Breakdown",
        font=("Arial", 16, "bold")
    )
    threat_breakdown_title.pack(anchor="w", padx=20, pady=10)

    # Create a simple pie chart representation
    pie_frame = customtkinter.CTkFrame(master=threat_breakdown_frame, fg_color="transparent")
    pie_frame.pack(fill="x", padx=20, pady=10)

    # Left side for pie chart
    pie_chart_frame = customtkinter.CTkFrame(master=pie_frame)
    pie_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Canvas for pie chart
    pie_canvas = tk.Canvas(pie_chart_frame, bg="#1c253a", highlightthickness=0)
    pie_canvas.pack(fill="both", expand=True, padx=20, pady=20)

    # Right side for legend
    legend_frame = customtkinter.CTkFrame(master=pie_frame)
    legend_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

    # Generate data for pie chart
    threat_types = {
        "Malware": {"count": random.randint(30, 60), "color": "#1b720f"},
        "Phishing": {"count": random.randint(20, 40), "color": "#714bae"},
        "Ransomware": {"count": random.randint(10, 25), "color": "#63003d"},
        "Trojan": {"count": random.randint(15, 30), "color": "#2a6f1e"},
        "Spyware": {"count": random.randint(10, 20), "color": "#116805"},
        "Zero-day": {"count": random.randint(5, 15), "color": "#4e288b"}
    }

    # Calculate total and percentages
    total_threats = sum(threat["count"] for threat in threat_types.values())

    # Draw pie chart
    def draw_pie_chart():
        pie_canvas.delete("all")

        center_x, center_y = 150, 150
        radius = 100

        start_angle = 0

        for threat_type, data in threat_types.items():
            # Calculate angle based on percentage
            angle = (data["count"] / total_threats) * 360
            end_angle = start_angle + angle

            # Draw pie slice
            pie_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle,
                fill=data["color"], outline="#323b50", width=2
            )

            start_angle = end_angle

    draw_pie_chart()

    # Draw legend
    legend_title = customtkinter.CTkLabel(
        master=legend_frame,
        text="Threat Types",
        font=("Arial", 14, "bold")
    )
    legend_title.pack(anchor="w", padx=20, pady=(20, 10))

    for threat_type, data in threat_types.items():
        # Create a row for each threat type
        threat_row = customtkinter.CTkFrame(master=legend_frame, fg_color="transparent")
        threat_row.pack(fill="x", padx=20, pady=5)

        # Color indicator
        color_indicator = customtkinter.CTkFrame(
            master=threat_row,
            width=15,
            height=15,
            corner_radius=2,
            fg_color=data["color"]
        )
        color_indicator.pack(side="left", padx=(0, 10))

        # Threat type name
        threat_name = customtkinter.CTkLabel(
            master=threat_row,
            text=threat_type,
            font=("Arial", 12)
        )
        threat_name.pack(side="left")

        # Count and percentage
        percentage = (data["count"] / total_threats) * 100
        count_text = f"{data['count']} ({percentage:.1f}%)"

        count_label = customtkinter.CTkLabel(
            master=threat_row,
            text=count_text,
            font=("Arial", 12)
        )
        count_label.pack(side="right")

    # ======= TIME PERIOD SELECTOR =======
    # Add a time period selector at the top (just UI elements for now)
    time_frame = customtkinter.CTkFrame(master=main_content)
    time_frame.pack(fill="x", padx=10, pady=(0, 10))

    time_label = customtkinter.CTkLabel(
        master=time_frame,
        text="Time Period:",
        font=("Arial", 14)
    )
    time_label.pack(side="left", padx=20, pady=10)

    time_periods = ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom Range"]

    time_var = tk.StringVar(value="Last 30 Days")
    time_dropdown = customtkinter.CTkComboBox(
        master=time_frame,
        values=time_periods,
        variable=time_var,
        width=200
    )
    time_dropdown.pack(side="left", padx=10, pady=10)

    refresh_button = customtkinter.CTkButton(
        master=time_frame,
        text="Refresh Data",
        width=120
    )
    refresh_button.pack(side="right", padx=20, pady=10)

    # Add export button
    export_button = customtkinter.CTkButton(
        master=time_frame,
        text="Export Report",
        width=120,
        fg_color="#586b78"
    )
    export_button.pack(side="right", padx=10, pady=10)