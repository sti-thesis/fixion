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


def create_stats_card(parent, title, value, icon_name, row, column):
    """Create a single statistics card"""
    card = customtkinter.CTkFrame(parent, corner_radius=10)
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
    customtkinter.CTkLabel(card, text=title, font=("Arial", 14)).pack(anchor="w", padx=15, pady=5)
    customtkinter.CTkLabel(card, text=value, font=("Arial", 24, "bold")).pack(anchor="w", padx=15, pady=(5, 15))


def create_threat_chart(parent, threat_data):
    """Create threat detection trend chart"""
    # Count threats by date
    threat_counts = {}
    for threat in threat_data:
        date = threat["date"]
        threat_counts[date] = threat_counts.get(date, 0) + 1

    # Sort dates and prepare chart data
    sorted_dates = sorted(threat_counts.keys())
    chart_dates = [date if i % 5 == 0 else "" for i, date in enumerate(sorted_dates)]
    chart_values = [threat_counts[date] for date in sorted_dates]
    max_value = max(chart_values) if chart_values else 10

    # Create chart canvas
    chart_canvas = tk.Canvas(parent, bg="#1c253a", highlightthickness=0, height=150)
    chart_canvas.pack(fill="x", padx=20, pady=10)

    def draw_chart():
        chart_canvas.delete("all")
        chart_width = chart_canvas.winfo_width() or 900
        chart_height = 150
        bar_spacing = chart_width / (len(chart_values) * 1.5) if chart_values else 1
        bottom_margin = 30

        # Draw axes
        chart_canvas.create_line(40, chart_height - bottom_margin, chart_width - 20,
                                 chart_height - bottom_margin, fill="#a9b8c4", width=2)
        chart_canvas.create_line(40, 20, 40, chart_height - bottom_margin, fill="#a9b8c4", width=2)

        # Draw bars
        for i, value in enumerate(chart_values):
            bar_height = (value / max_value) * (chart_height - bottom_margin - 30)
            x1 = 50 + (i * bar_spacing * 1.5)
            y1 = chart_height - bottom_margin - bar_height
            x2 = x1 + bar_spacing
            y2 = chart_height - bottom_margin

            color = f"#{int(min(255, 100 + (155 * value / max_value))):02x}4080"
            chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            # Add date labels
            if chart_dates[i]:
                chart_canvas.create_text(x1 + bar_spacing / 2, chart_height - bottom_margin + 15,
                                         text=chart_dates[i][5:], fill="#a9b8c4", font=("Arial", 8))

        # Y-axis labels
        for i in range(5):
            value = int(max_value * i / 4)
            y_pos = chart_height - bottom_margin - (i * (chart_height - bottom_margin - 30) / 4)
            chart_canvas.create_text(30, y_pos, text=str(value), fill="#a9b8c4", font=("Arial", 8))

    chart_canvas.bind("<Configure>", lambda e: draw_chart())
    chart_canvas.after(100, draw_chart)  # Initial draw


def create_client_table(parent, clients):
    """Create client activity table"""
    if not clients:
        customtkinter.CTkLabel(parent, text="No client machines found. Add clients in User Management.",
                               font=("Arial", 12)).pack(pady=20)
        return

    # Table headers
    header_frame = customtkinter.CTkFrame(parent, fg_color="#323b50")
    header_frame.pack(fill="x", pady=(0, 2))

    headers = ["Client Name", "Status", "Last Active", "Threats Detected", "Protection Status"]
    for i, header in enumerate(headers):
        customtkinter.CTkLabel(header_frame, text=header, font=("Arial", 12, "bold")).grid(
            row=0, column=i, padx=15, pady=10, sticky="w")
        header_frame.grid_columnconfigure(i, weight=1)

    # Table rows
    for client in clients:
        row_frame = customtkinter.CTkFrame(parent)
        row_frame.pack(fill="x", pady=1)

        # Client name
        customtkinter.CTkLabel(row_frame, text=client.get("username", "Unknown"),
                               font=("Arial", 12)).grid(row=0, column=0, padx=15, pady=10, sticky="w")

        # Status with indicator
        status_text = "Online" if client.get("active", True) else "Offline"
        status_color = "#1b720f" if client.get("active", True) else "#63003d"

        status_container = customtkinter.CTkFrame(row_frame, fg_color="transparent")
        status_container.grid(row=0, column=1, padx=15, pady=10, sticky="w")

        # Status indicator dot
        customtkinter.CTkFrame(status_container, width=12, height=12, corner_radius=6,
                               fg_color=status_color).pack(side="left", padx=(0, 5))
        customtkinter.CTkLabel(status_container, text=status_text, font=("Arial", 12)).pack(side="left")

        # Last active
        if client.get("active", True):
            last_active_text = "Now"
        else:
            minutes_ago = random.randint(60, 10080)
            if minutes_ago > 1440:  # More than 24 hours
                last_active_text = f"{minutes_ago // 1440} days ago"
            else:
                last_active_text = f"{minutes_ago // 60} hours ago"

        customtkinter.CTkLabel(row_frame, text=last_active_text, font=("Arial", 12)).grid(
            row=0, column=2, padx=15, pady=10, sticky="w")

        # Threats detected
        customtkinter.CTkLabel(row_frame, text=str(random.randint(0, 20)), font=("Arial", 12)).grid(
            row=0, column=3, padx=15, pady=10, sticky="w")

        # Protection status
        protection_status = random.choice(["Protected", "Update Required", "Protected"])
        protection_color = "#1b720f" if protection_status == "Protected" else "#714bae"
        customtkinter.CTkLabel(row_frame, text=protection_status, text_color=protection_color,
                               font=("Arial", 12)).grid(row=0, column=4, padx=15, pady=10, sticky="w")

        # Configure equal column widths
        for col in range(5):
            row_frame.grid_columnconfigure(col, weight=1)


def create_pie_chart(canvas, threat_types, total_threats):
    """Draw pie chart on canvas"""
    canvas.delete("all")
    center_x, center_y, radius = 150, 150, 100
    start_angle = 0

    for threat_type, data in threat_types.items():
        angle = (data["count"] / total_threats) * 360
        canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                          start=start_angle, extent=angle, fill=data["color"], outline="#323b50", width=2)
        start_angle += angle


def create_legend(parent, threat_types, total_threats):
    """Create legend for pie chart"""
    customtkinter.CTkLabel(parent, text="Threat Types", font=("Arial", 14, "bold")).pack(
        anchor="w", padx=20, pady=(20, 10))

    for threat_type, data in threat_types.items():
        # Create row container
        row = customtkinter.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=5)

        # Color indicator
        customtkinter.CTkFrame(row, width=15, height=15, corner_radius=2,
                               fg_color=data["color"]).pack(side="left", padx=(0, 10))

        # Threat type name
        customtkinter.CTkLabel(row, text=threat_type, font=("Arial", 12)).pack(side="left")

        # Count and percentage
        percentage = (data["count"] / total_threats) * 100
        customtkinter.CTkLabel(row, text=f"{data['count']} ({percentage:.1f}%)",
                               font=("Arial", 12)).pack(side="right")


def open_analytics_page(parent_frame):
    """Analytics dashboard page with charts and statistics"""
    # Clear the frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="Analytics",
        font=("Roboto", 24, "bold"),
        text_color= "#e9e8e8"
    )
    title.pack(anchor="w", padx=12, pady= 12)

    # Main scrollable content
    main_content = customtkinter.CTkScrollableFrame(parent_frame, width=950, height=800, fg_color="#22222f")
    main_content.pack(fill="both", expand=True, padx=20, pady=10)

    # ======= TOP CONTROLS =======
    controls = customtkinter.CTkFrame(main_content)
    controls.pack(fill="x", padx=10, pady=(0, 10))

    customtkinter.CTkLabel(controls, text="Time Period:", font=("Arial", 14)).pack(
        side="left", padx=20, pady=10)

    time_periods = ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom Range"]
    time_var = tk.StringVar(value="Last 30 Days")
    customtkinter.CTkComboBox(controls, values=time_periods, variable=time_var, width=200).pack(
        side="left", padx=10, pady=10)

    customtkinter.CTkButton(controls, text="Export Report", width=120, fg_color="#586b78").pack(
        side="right", padx=10, pady=10)
    customtkinter.CTkButton(controls, text="Refresh Data", width=120).pack(
        side="right", padx=20, pady=10)

    # ======= STATISTICS CARDS =======
    stats_section = customtkinter.CTkFrame(main_content)
    stats_section.pack(fill="x", padx=10, pady=10)

    # Configure grid for equal column distribution
    for i in range(4):
        stats_section.grid_columnconfigure(i, weight=1)

    # Create stats cards
    stats_data = [
        ("Total Threats Detected", str(random.randint(120, 300)), "threat_logs_icon.png"),
        ("Active Clients", str(len(get_client_machines())), "client_machine_icon.png"),
        ("Resolved Threats", str(random.randint(100, 250)), "systems_icon.png"),
        ("Critical Alerts", str(random.randint(5, 20)), "analytics_icon.png")
    ]

    for i, (title, value, icon) in enumerate(stats_data):
        create_stats_card(stats_section, title, value, icon, 0, i)

    # ======= THREAT DETECTION CHART =======
    chart_section = customtkinter.CTkFrame(main_content)
    chart_section.pack(fill="x", padx=10, pady=10)

    customtkinter.CTkLabel(chart_section, text="Threat Detection Trend (30 Days)",
                           font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)

    threat_data = generate_mock_threat_data(30)
    create_threat_chart(chart_section, threat_data)

    # ======= CLIENT ACTIVITY TABLE =======
    clients_section = customtkinter.CTkFrame(main_content)
    clients_section.pack(fill="x", padx=10, pady=10)

    customtkinter.CTkLabel(clients_section, text="Client Machine Activity",
                           font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)

    table_container = customtkinter.CTkFrame(clients_section)
    table_container.pack(fill="x", padx=20, pady=10)

    create_client_table(table_container, get_client_machines())

    # ======= THREAT BREAKDOWN =======
    breakdown_section = customtkinter.CTkFrame(main_content)
    breakdown_section.pack(fill="x", padx=10, pady=10)

    customtkinter.CTkLabel(breakdown_section, text="Threat Type Breakdown",
                           font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)

    # Pie chart and legend container
    pie_container = customtkinter.CTkFrame(breakdown_section, fg_color="transparent")
    pie_container.pack(fill="x", padx=20, pady=10)

    # Pie chart
    pie_chart_section = customtkinter.CTkFrame(pie_container)
    pie_chart_section.pack(side="left", fill="both", expand=True, padx=(0, 10))

    pie_canvas = tk.Canvas(pie_chart_section, bg="#1c253a", highlightthickness=0)
    pie_canvas.pack(fill="both", expand=True, padx=20, pady=20)

    # Legend
    legend_section = customtkinter.CTkFrame(pie_container)
    legend_section.pack(side="right", fill="both", expand=True, padx=(10, 0))

    # Generate threat type data
    threat_types = {
        "Malware": {"count": random.randint(30, 60), "color": "#1b720f"},
        "Phishing": {"count": random.randint(20, 40), "color": "#714bae"},
        "Ransomware": {"count": random.randint(10, 25), "color": "#63003d"},
        "Trojan": {"count": random.randint(15, 30), "color": "#2a6f1e"},
        "Spyware": {"count": random.randint(10, 20), "color": "#116805"},
        "Zero-day": {"count": random.randint(5, 15), "color": "#4e288b"}
    }

    total_threats = sum(threat["count"] for threat in threat_types.values())

    # Draw pie chart and create legend
    pie_canvas.after(100, lambda: create_pie_chart(pie_canvas, threat_types, total_threats))
    create_legend(legend_section, threat_types, total_threats)