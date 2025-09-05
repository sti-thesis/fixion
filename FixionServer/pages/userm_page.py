import customtkinter
import json
import os
import tkinter as tk
from tkinter import messagebox


def open_userm_page(parent_frame):
    """
    User Management page with consistent theme
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="User Management",
        font=("Roboto", 24, "bold"),
        text_color="#e9e8e8"
    )
    title.pack(anchor="w", padx=(12,0), pady=(12,0))

    # Search and filter section - directly on parent frame
    search_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent", border_width=0)
    search_frame.pack(fill="x", padx=(30,0), pady=(18,0))

    search_entry = customtkinter.CTkEntry(
        master=search_frame,
        placeholder_text="Search users...",
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

    # Filter dropdown for user types
    filter_var = tk.StringVar(value="All")
    filter_combobox = customtkinter.CTkComboBox(
        master=search_frame,
        width=120,
        values=["All", "Users", "Client Machines", "Admins", "IT Staff"],
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

    # Main content frame
    content_frame = customtkinter.CTkFrame(master=parent_frame, fg_color="#15141b")
    content_frame.pack(fill="both", expand=True, padx=30, pady=12)

    # Create two sections: User list on left, Add/Edit form on right
    list_frame = customtkinter.CTkFrame(master=content_frame, fg_color="#22232e", border_width=0, corner_radius=20)
    list_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

    form_frame = customtkinter.CTkFrame(master=content_frame, fg_color="#22232e", border_width=0, corner_radius=20)
    form_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

    # ======= USER LIST SECTION =======
    list_label = customtkinter.CTkLabel(
        master=list_frame,
        text="User List",
        text_color="#e9e8e8",
        font=("Roboto", 18, "bold")
    )
    list_label.pack(pady=10, anchor="w", padx=10)

    # User list display with scrollbar
    user_list_container = customtkinter.CTkScrollableFrame(
        master=list_frame,
        width=400,
        height=500,
        scrollbar_button_color="#565B73",
        scrollbar_button_hover_color="#6B7089",
        border_width=0,
        fg_color="#22222f"
    )
    user_list_container.pack(fill="both", expand=True, padx=4, pady=(0,20))

    # ======= ADD/EDIT USER FORM =======
    form_label = customtkinter.CTkLabel(
        master=form_frame,
        text="Add New User",
        text_color="#e9e8e8",
        font=("Roboto", 18, "bold")
    )
    form_label.pack(pady=10, anchor="w", padx=10)

    # Form fields container
    fields_frame = customtkinter.CTkFrame(master=form_frame, fg_color="transparent", border_width=0)
    fields_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # User type selection (User vs Client Machine)
    type_frame = customtkinter.CTkFrame(master=fields_frame, fg_color="transparent", border_width=0)
    type_frame.pack(fill="x", pady=10)

    type_label = customtkinter.CTkLabel(
        master=type_frame,
        text="Type:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    type_label.pack(side="left")

    type_var = tk.StringVar(value="User")
    type_combobox = customtkinter.CTkComboBox(
        master=type_frame,
        width=180,
        values=["User", "Client Machine"],
        variable=type_var,
        border_width=0,
        fg_color="#293046",
        button_color="#293046",
        dropdown_fg_color="#293046",
        dropdown_font=("Roboto Medium", 12),
        dropdown_text_color="#e9e8e8",
        corner_radius=12,
        text_color="#b1b4c9",
    )
    type_combobox.pack(side="left", padx=10)

    # User section - contains fields for human users
    user_section = customtkinter.CTkFrame(master=fields_frame, fg_color="transparent", border_width=0)
    user_section.pack(fill="x", pady=10)

    # First Name field
    firstname_frame = customtkinter.CTkFrame(master=user_section, fg_color="transparent", border_width=0)
    firstname_frame.pack(fill="x", pady=5)

    firstname_label = customtkinter.CTkLabel(
        master=firstname_frame,
        text="First Name:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    firstname_label.pack(side="left")

    firstname_entry = customtkinter.CTkEntry(
        master=firstname_frame,
        width=270,
        border_width=0,
        fg_color="#293046",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12

    )
    firstname_entry.pack(side="left", padx=10)

    # Last Name field
    lastname_frame = customtkinter.CTkFrame(master=user_section, fg_color="transparent", border_width=0)
    lastname_frame.pack(fill="x", pady=5)

    lastname_label = customtkinter.CTkLabel(
        master=lastname_frame,
        text="Last Name:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    lastname_label.pack(side="left")

    lastname_entry = customtkinter.CTkEntry(
        master=lastname_frame,
        width=270,
        border_width=0,
        fg_color="#293046",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12
    )
    lastname_entry.pack(side="left", padx=10)

    # Username field
    username_frame = customtkinter.CTkFrame(master=user_section, fg_color="transparent", border_width=0)
    username_frame.pack(fill="x", pady=5)

    username_label = customtkinter.CTkLabel(
        master=username_frame,
        text="Username:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    username_label.pack(side="left")

    username_entry = customtkinter.CTkEntry(
        master=username_frame,
        width=270,
        border_width=0,
        fg_color="#293046",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12
    )
    username_entry.pack(side="left", padx=10)

    # Password field
    password_frame = customtkinter.CTkFrame(master=user_section, fg_color="transparent", border_width=0)
    password_frame.pack(fill="x", pady=5)

    password_label = customtkinter.CTkLabel(
        master=password_frame,
        text="Password:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    password_label.pack(side="left")

    password_entry = customtkinter.CTkEntry(
        master=password_frame,
        width=270,
        show="*",
        border_width=0,
        fg_color="#293046",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12
    )
    password_entry.pack(side="left", padx=10)

    # Role selection
    role_frame = customtkinter.CTkFrame(master=user_section, fg_color="transparent", border_width=0)
    role_frame.pack(fill="x", pady=5)

    role_label = customtkinter.CTkLabel(
        master=role_frame,
        text="Role:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    role_label.pack(side="left")

    role_var = tk.StringVar(value="admin")
    role_combobox = customtkinter.CTkComboBox(
        master=role_frame,
        width=180,
        values=["admin", "it staff", "viewer"],
        variable=role_var,
        border_width=0,
        fg_color="#293046",
        button_color="#293046",
        dropdown_fg_color="#293046",
        dropdown_font=("Roboto Medium", 12),
        dropdown_text_color="#e9e8e8",
        corner_radius=12,
        text_color="#b1b4c9"
    )
    role_combobox.pack(side="left", padx=10)

    # Client machine section - contains fields for computer entries
    client_section = customtkinter.CTkFrame(master=fields_frame, fg_color="transparent", border_width=0)

    # Computer name field
    computer_frame = customtkinter.CTkFrame(master=client_section, fg_color="transparent", border_width=0)
    computer_frame.pack(fill="x", pady=10)

    computer_label = customtkinter.CTkLabel(
        master=computer_frame,
        text="Computer Name:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    computer_label.pack(side="left")

    computer_entry = customtkinter.CTkEntry(
        master=computer_frame,
        width=270,
        border_width=0,
        fg_color="#293046",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12
    )
    computer_entry.pack(side="left", padx=10)

    # Location field
    location_frame = customtkinter.CTkFrame(master=client_section, fg_color="transparent", border_width=0)
    location_frame.pack(fill="x", pady=5)

    location_label = customtkinter.CTkLabel(
        master=location_frame,
        text="Location:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    location_label.pack(side="left")

    location_entry = customtkinter.CTkEntry(
        master=location_frame,
        width=270,
        border_width=0,
        fg_color="#293046",
        text_color="#e9e8e8",
        placeholder_text_color="#b1b4c9",
        corner_radius=12
    )
    location_entry.pack(side="left", padx=10)

    # Status frame (common for both users and clients)
    status_frame = customtkinter.CTkFrame(master=fields_frame, fg_color="transparent", border_width=0)
    status_frame.pack(fill="x", pady=10)

    status_label = customtkinter.CTkLabel(
        master=status_frame,
        text="Status:",
        width=100,
        text_color="#e9e8e8",
        font=("Roboto", 12, "bold"),
        anchor="w"
    )
    status_label.pack(side="left")

    status_var = tk.BooleanVar(value=True)
    status_switch = customtkinter.CTkSwitch(
        master=status_frame,
        text="Active",
        variable=status_var,
        onvalue=True,
        offvalue=False,
        text_color="#e9e8e8",
        font=("Roboto", 12)
    )
    status_switch.pack(side="left", padx=10)

    # Button frame
    button_frame = customtkinter.CTkFrame(master=fields_frame, fg_color="transparent", border_width=0)
    button_frame.pack(fill="x", pady=20)

    # Function to toggle between user and client machine forms
    def toggle_form_type(choice):
        if choice == "User":
            client_section.pack_forget()
            user_section.pack(fill="x", pady=10, after=type_frame)
            form_label.configure(text="Add New User")
        else:
            user_section.pack_forget()
            client_section.pack(fill="x", pady=10, after=type_frame)
            form_label.configure(text="Add Client Machine")

    type_combobox.configure(command=toggle_form_type)

    # Reset form function
    def reset_form():
        # Reset all entries
        firstname_entry.delete(0, 'end')
        lastname_entry.delete(0, 'end')
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        computer_entry.delete(0, 'end')
        location_entry.delete(0, 'end')

        # Reset selections
        type_combobox.set("User")
        role_combobox.set("admin")
        status_var.set(True)

        # Reset form state
        toggle_form_type("User")
        form_label.configure(text="Add New User")
        save_button.configure(text="Add User")

        # Reset editing state
        global currently_editing
        currently_editing = None

    reset_button = customtkinter.CTkButton(
        master=button_frame,
        text="Reset",
        width=100,
        fg_color="#565B73",
        hover_color="#6B7089",
        corner_radius=28,
        command=reset_form
    )
    reset_button.pack(side="left", padx=(0, 10))

    # Save function and button
    global currently_editing
    currently_editing = None

    def save_user():
        # Get form type (User or Client Machine)
        form_type = type_combobox.get()

        # Load current users
        users = load_users()

        # Common fields
        active = status_var.get()

        if form_type == "User":
            # Process user form
            first_name = firstname_entry.get().strip()
            last_name = lastname_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            role = role_combobox.get()

            # Validation
            if not username:
                messagebox.showerror("Error", "Username is required!")
                return

            if not first_name or not last_name:
                messagebox.showerror("Error", "First and last name are required!")
                return

            if not currently_editing and not password:
                messagebox.showerror("Error", "Password is required for new users!")
                return

            # Prepare user data
            user_data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "active": active,
                "type": "user"
            }

            # Add password if provided (in real app, hash it)
            if password:
                user_data["password"] = password

        else:
            # Process client machine form
            computer_name = computer_entry.get().strip()
            location = location_entry.get().strip()

            # Validation
            if not computer_name:
                messagebox.showerror("Error", "Computer name is required!")
                return

            # Prepare client data - using computer_name as both username and name
            user_data = {
                "username": computer_name,  # Use computer name as username
                "first_name": computer_name,
                "last_name": "Computer",
                "role": "client machine",
                "active": active,
                "type": "client",
                "location": location
            }

        if currently_editing is not None:
            # Editing existing user/client
            edited = False
            for user in users:
                if user["id"] == currently_editing:
                    # Update the user/client with new data
                    # Preserve ID and any fields not in the form
                    user_data["id"] = currently_editing

                    # Special handling for password - don't overwrite if empty
                    if form_type == "User" and not password and "password" in user:
                        user_data["password"] = user["password"]

                    # Update the user entry with new data
                    for key, value in user_data.items():
                        user[key] = value

                    edited = True
                    break

            if not edited:
                messagebox.showerror("Error", "User not found!")
                return

            message = f"{'User' if form_type == 'User' else 'Client machine'} updated successfully!"
        else:
            # Adding new user/client
            # Check if username already exists
            for user in users:
                if user["username"] == user_data["username"]:
                    messagebox.showerror("Error",
                                         f"{'Username' if form_type == 'User' else 'Computer name'} already exists!")
                    return

            # Add ID to new user
            new_id = max([user["id"] for user in users], default=0) + 1
            user_data["id"] = new_id

            # Add new user/client to list
            users.append(user_data)
            message = f"{'User' if form_type == 'User' else 'Client machine'} added successfully!"

        # Save users to file
        save_users(users)

        # Reset form and refresh list
        reset_form()
        refresh_user_list()

        # Show success message
        messagebox.showinfo("Success", message)

    save_button = customtkinter.CTkButton(
        master=button_frame,
        text="Add User",
        width=150,
        corner_radius=28,
        command=save_user
    )
    save_button.pack(side="right", padx=10)

    # ======= USER LIST FUNCTIONS =======
    def load_users():
        """Load users from the JSON file"""
        try:
            with open('users.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty list if file doesn't exist or is invalid
            return []

    def save_users(users):
        """Save users to the JSON file"""
        with open('users.json', 'w') as file:
            json.dump(users, file)

    def refresh_user_list():
        """Refresh the user list display"""
        # Clear current list
        for widget in user_list_container.winfo_children():
            widget.destroy()

        # Load users
        users = load_users()

        # Filter users if search is active
        search_term = search_entry.get().lower()
        if search_term:
            users = [user for user in users if
                     search_term in user.get("username", "").lower() or
                     search_term in user.get("first_name", "").lower() or
                     search_term in user.get("last_name", "").lower() or
                     search_term in user.get("role", "").lower()]

        # Apply filter
        filter_choice = filter_var.get()
        if filter_choice == "Users":
            users = [u for u in users if u.get("role") != "client machine"]
        elif filter_choice == "Client Machines":
            users = [u for u in users if u.get("role") == "client machine"]
        elif filter_choice == "Admins":
            users = [u for u in users if u.get("role") == "admin"]
        elif filter_choice == "IT Staff":
            users = [u for u in users if u.get("role") == "it staff"]

        # Sort users: clients first, then users by role
        def sort_key(user):
            # Client machines first, then by role importance
            if user.get("role") == "client machine":
                return (0, user.get("username", "").lower())

            # Then admins
            if user.get("role") == "admin":
                return (1, user.get("username", "").lower())

            # Then IT staff
            if user.get("role") == "it staff":
                return (2, user.get("username", "").lower())

            # Then others
            return (3, user.get("username", "").lower())

        users.sort(key=sort_key)

        # Display users
        for i, user in enumerate(users):
            # Create a frame for this user row
            user_frame = customtkinter.CTkFrame(
                master=user_list_container,
                fg_color="#283146",
                corner_radius=12,
                height=60
            )
            user_frame.pack(fill="x", pady=5, padx=8)

            # Status indicator (colored dot)
            status_color = "#1b720f" if user.get("active", True) else "#63003d"
            status_indicator = customtkinter.CTkFrame(
                master=user_frame,
                width=12,
                height=12,
                corner_radius=6,
                fg_color=status_color
            )
            status_indicator.pack(side="left", padx=(10, 8), pady=10)

            # User info container
            info_container = customtkinter.CTkFrame(master=user_frame, fg_color="transparent", border_width=0)
            info_container.pack(side="left", fill="both", expand=True, padx=5, pady=10)

            # Username and role
            if user.get("role") == "client machine":
                display_text = f"🖥️ {user.get('username')} (Client)"
                role_color = "#748498"
            else:
                display_text = f"👤 {user.get('username')} ({user.get('role', 'unknown')})"
                role_color = "#e9e8e8"

            username_label = customtkinter.CTkLabel(
                master=info_container,
                text=display_text,
                font=("Roboto", 12, "bold"),
                text_color="#e9e8e8",
                anchor="w"
            )
            username_label.pack(anchor="w")

            # For users, show full name; for clients, show location
            if user.get("role") != "client machine":
                name_text = f"{user.get('first_name', '')} {user.get('last_name', '')}"
                if name_text.strip():
                    name_label = customtkinter.CTkLabel(
                        master=info_container,
                        text=name_text,
                        font=("Roboto", 10),
                        text_color="#b1b4c9",
                        anchor="w"
                    )
                    name_label.pack(anchor="w")
            else:
                if user.get("location"):
                    location_text = f"📍 {user.get('location')}"
                    location_label = customtkinter.CTkLabel(
                        master=info_container,
                        text=location_text,
                        font=("Roboto", 10),
                        text_color="#b1b4c9",
                        anchor="w"
                    )
                    location_label.pack(anchor="w")

            # Button container
            button_container = customtkinter.CTkFrame(master=user_frame, fg_color="transparent", border_width=0)
            button_container.pack(side="right", padx=10, pady=10)

            # Edit button
            edit_button = customtkinter.CTkButton(
                master=button_container,
                text="Edit",
                width=60,
                height=25,
                corner_radius=20,
                font=("Roboto", 10),
                command=lambda u=user: edit_user(u)
            )
            edit_button.pack(side="right", padx=(5, 0))

            # Delete button
            delete_button = customtkinter.CTkButton(
                master=button_container,
                text="Delete",
                width=60,
                height=25,
                corner_radius=20,
                font=("Roboto", 10),
                fg_color="#63003d",
                hover_color="#7a0049",
                command=lambda u=user: delete_user(u)
            )
            delete_button.pack(side="right", padx=(5, 5))

    def edit_user(user):
        """Populate the form with user data for editing"""
        global currently_editing
        currently_editing = user["id"]

        # Determine if this is a client machine or user
        is_client = user.get("role") == "client machine"

        # Set form type
        type_combobox.set("Client Machine" if is_client else "User")
        toggle_form_type("Client Machine" if is_client else "User")

        if is_client:
            # Set client machine fields
            computer_entry.delete(0, 'end')
            computer_entry.insert(0, user.get("first_name", ""))

            location_entry.delete(0, 'end')
            location_entry.insert(0, user.get("location", ""))
        else:
            # Set user fields
            firstname_entry.delete(0, 'end')
            firstname_entry.insert(0, user.get("first_name", ""))

            lastname_entry.delete(0, 'end')
            lastname_entry.insert(0, user.get("last_name", ""))

            username_entry.delete(0, 'end')
            username_entry.insert(0, user.get("username", ""))

            password_entry.delete(0, 'end')
            # Password field left empty when editing

            role_combobox.set(user.get("role", "admin"))

        # Set common fields
        status_var.set(user.get("active", True))

        # Update form title
        if is_client:
            form_label.configure(text=f"Edit Client: {user.get('username')}")
        else:
            form_label.configure(text=f"Edit User: {user.get('username')}")

        save_button.configure(text="Update")

    def delete_user(user):
        """Delete a user after confirmation"""
        username = user.get("username", "Unknown")
        user_type = "client machine" if user.get("role") == "client machine" else "user"

        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the {user_type} '{username}'?"
        )

        if confirm:
            # Load users
            users = load_users()

            # Remove user with matching ID
            users = [u for u in users if u["id"] != user["id"]]

            # Save updated list
            save_users(users)

            # Refresh display
            refresh_user_list()

            # Show success message
            messagebox.showinfo("Success", f"{user_type.capitalize()} '{username}' deleted successfully!")

    # Connect search and filter functions
    search_button.configure(command=refresh_user_list)
    search_entry.bind("<Return>", lambda event: refresh_user_list())
    filter_combobox.configure(command=lambda _: refresh_user_list())
    refresh_button.configure(command=refresh_user_list)

    # Initial form setup
    toggle_form_type("User")

    # Initial list population
    refresh_user_list()