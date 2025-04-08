import customtkinter
import tkinter
from tkinter import messagebox


def center_window(window, width, height):
    """Centers a tkinter window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def open_signup_page(current_window):
    current_window.withdraw()

    signup = customtkinter.CTk()
    signup.title("Signup Page")

    # Set dimensions and center the window
    width, height = 500, 700  # Increased height to accommodate extra field
    center_window(signup, width, height)

    def process_signup():
        first_name = firstname_entry.get()
        last_name = lastname_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = password2_entry.get()

        # validation
        if not all([first_name, last_name, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        if not check_box.get():
            messagebox.showerror("Error", "You must agree to the Terms of Service and Privacy Policy!")
            return

        # Build full name from first and last name
        full_name = f"{first_name} {last_name}"
        messagebox.showinfo("Success", f"Account created for {username}!")
        signup.after(100, lambda: safe_destroy_and_show(signup, current_window))

    # to return to login page
    def back_to_login():
        signup.after(100, lambda: safe_destroy_and_show(signup, current_window))

    def safe_destroy_and_show(window_to_destroy, window_to_show):
        try:
            window_to_destroy.destroy()
            window_to_show.deiconify()
        except Exception as e:
            print(f"Error during window transition: {e}")

    # Main frame
    frame = customtkinter.CTkFrame(master=signup, width=400, height=600, corner_radius=18)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Logo placeholder
    logo = customtkinter.CTkFrame(master=frame, width=150, height=150)
    logo.place(relx=0.5, rely=0.18, anchor=tkinter.CENTER)

    # Title label
    label_1 = customtkinter.CTkLabel(master=frame, fg_color="transparent", text="Create an Admin Account")
    label_1.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

    # Create a frame to hold the first name and last name entries with completely transparent background
    name_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent", border_width=0)
    name_frame.place(relx=0.5, rely=0.43, anchor=tkinter.CENTER)

    # First name entry - using transparent background
    firstname_entry = customtkinter.CTkEntry(master=name_frame, width=145, fg_color="transparent",
                                             placeholder_text='First Name')
    firstname_entry.grid(row=0, column=0, padx=(0, 5))

    # Last name entry - using transparent background
    lastname_entry = customtkinter.CTkEntry(master=name_frame, width=145, fg_color="transparent",
                                            placeholder_text='Last Name')
    lastname_entry.grid(row=0, column=1, padx=(5, 0))

    # Username entry
    username_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",
                                            placeholder_text='Username')
    username_entry.place(relx=0.5, rely=0.51, anchor=tkinter.CENTER)

    # Password entry
    password_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",
                                            placeholder_text='Password', show="*")
    password_entry.place(relx=0.5, rely=0.59, anchor=tkinter.CENTER)

    # Confirm password entry
    password2_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",
                                             placeholder_text='Confirm Password', show="*")
    password2_entry.place(relx=0.5, rely=0.67, anchor=tkinter.CENTER)

    # Terms checkbox
    check_box = customtkinter.CTkCheckBox(master=frame, checkbox_height=20, checkbox_width=20, border_width=2,
                                          text="I agree to the Terms of Service and Privacy Policy")
    check_box.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

    # Sign up button
    signup_btn = customtkinter.CTkButton(master=frame, width=230, text="Sign Up", command=process_signup)
    signup_btn.place(relx=0.5, rely=0.83, anchor=tkinter.CENTER)

    # Login button
    login_btn = customtkinter.CTkButton(master=frame, width=230, text="Already Have an Account? Login", border_width=2,
                                        fg_color="transparent", text_color="#ECEFF1", command=back_to_login)
    login_btn.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    signup.protocol("WM_DELETE_WINDOW", back_to_login)
    signup.mainloop()


if __name__ == "__main__":
    # testing lang para sa signup
    root = customtkinter.CTk()
    root.withdraw()
    open_signup_page(root)