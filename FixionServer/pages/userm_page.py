import customtkinter


def open_userm_page(parent_frame):
    """
    User Management page
    """
    # Clear the frame first
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Page title
    title = customtkinter.CTkLabel(
        master=parent_frame,
        text="User Management",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=20, anchor="w")

    # Empty content - to be filled as needed
    content = customtkinter.CTkLabel(
        master=parent_frame,
        text="User management content will be displayed here",
        font=("Arial", 14)
    )
    content.pack(pady=10, anchor="w")