import customtkinter
import tkinter
from tkinter import messagebox
import os
from PIL import Image

from signup_page import open_signup_page
from dashboard_page import open_dashboard_page


def center_window(window, width, height):
    """Centers a tkinter window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def validate_login(username, password):
    # For testing only
    if username == "1" and password == "1":
        return True, {"username": username, "role": "admin"}
    return False, None


def open_login_page():

    login = customtkinter.CTk(fg_color="#15141b")
    login.title('Login Page')

    # Set dimensions and center the window
    width, height = 700, 500
    center_window(login, width, height)

    def process_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        is_valid, user_info = validate_login(username, password)
        if is_valid:
            login.destroy()
            open_dashboard_page(user_info)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def open_forgot_password():
        messagebox.showinfo("Reset Password", "We will inform an admin that you forgot your password")

    frame = customtkinter.CTkFrame(master=login, width=450, height=460, corner_radius=18, fg_color="#122a3e")
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    label_1 = customtkinter.CTkLabel(
        master=frame,
        fg_color="transparent",
        text="Log into your Account",
        text_color="#e9e8e8",
        font=("Roboto Medium", 20, "bold")
    )
    label_1.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

    logo_path = os.path.join(os.path.dirname(__file__), "logo", "fixion_logo.png")
    logo_img = customtkinter.CTkImage(
        light_image=Image.open(logo_path),
        size=(160, 160)
    )
    logo_label = customtkinter.CTkLabel(
        master=frame,
        image=logo_img,
        text=""
    )
    logo_label.place(relx=0.5, rely=0.31, anchor=tkinter.CENTER)

    username_entry = customtkinter.CTkEntry(
        master=frame,
        width=300,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",        
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Enter Admin Username',

    )
    username_entry.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

    password_entry = customtkinter.CTkEntry(
        master=frame,
        width=300,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",        
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Enter Admin Password',
        show="*"
    )
    password_entry.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)

    forgot_label = customtkinter.CTkLabel(
        master=frame,
        fg_color="transparent",
        text_color="#e9e8e8",
        text="Forget password?",
        cursor="hand2"
    )
    forgot_label.place(relx=0.6, rely=0.68)
    forgot_label.bind("<Button-1>", lambda e: open_forgot_password())

    check_box = customtkinter.CTkCheckBox(
        master=frame,
        checkbox_height=18,
        checkbox_width=18,
        border_width=2,
        border_color="#15141b",
        hover_color="#15141b",
        fg_color="#15141b",
        corner_radius=12,
        text_color="#e9e8e8",
        text="Keep Me Login"
    )
    check_box.place(relx=0.17, rely=0.68)

    login_btn = customtkinter.CTkButton(
        master=frame,
        width=180,
        corner_radius=12,
        text_color="#e9e8e8",
        fg_color="#047eaf",
        hover_color="#22222f",
        text="Login",
        command=process_login
    )
    login_btn.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)

    signup_btn = customtkinter.CTkButton(
        master=frame,
        width=180,
        corner_radius=12,
        text_color="#e9e8e8",
        fg_color="#047eaf",
        hover_color="#22222f",
        text="Sign Up",
        command=lambda: open_signup_page(login)
    )
    signup_btn.place(relx=0.5, rely=0.88, anchor=tkinter.CENTER)
    login.mainloop()


if __name__ == "__main__":
    open_login_page()