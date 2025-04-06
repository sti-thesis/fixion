import customtkinter
import tkinter
from tkinter import messagebox
from customtkinter import set_default_color_theme


from signup_page import open_signup_window

from dashboard_page import open_dashboard_window


def validate_login(username, password):
    # buburahin din for testing lang
    if username == "admin" and password == "password":
        return True, {"username": username, "role": "admin"}
    return False, None

if __name__ == "__main__":
    try:
        set_default_color_theme("color_theme.json")
    except:
        print("Theme file not found. Using default theme.")

    login = customtkinter.CTk()
    login.geometry("700x500")
    login.title('Login Page')


    def process_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        is_valid, user_info = validate_login(username, password)
        if is_valid:
            login.destroy()
            open_dashboard_window(user_info)
        else:
            messagebox.showerror("Error", "Invalid username or password!")


    def open_forgot_password():
        messagebox.showinfo("Reset Password", "Password reset link has been sent to your email.")


    frame = customtkinter.CTkFrame(master=login, width=450, height=460, corner_radius=18)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    label_1 = customtkinter.CTkLabel(master=frame, fg_color="transparent", text="Log into your Account")
    label_1.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

    logo = customtkinter.CTkFrame(master=frame, width=150, height=150)
    logo.place(relx=0.5, rely=0.33, anchor=tkinter.CENTER)

    username_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",
                                            placeholder_text='Enter Admin Username')
    username_entry.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

    password_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",
                                            placeholder_text='Enter Admin Password', show="*")
    password_entry.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)

    forgot_label = customtkinter.CTkLabel(master=frame, fg_color="transparent", text="Forget password?", cursor="hand2")
    forgot_label.place(relx=0.6, rely=0.68)
    forgot_label.bind("<Button-1>", lambda e: open_forgot_password())

    check_box = customtkinter.CTkCheckBox(master=frame, checkbox_height=20, checkbox_width=20, border_width=2,
                                          text="Keep Me Login")
    check_box.place(relx=0.17, rely=0.68)

    login_btn = customtkinter.CTkButton(master=frame, width=180, text="Login", command=process_login)
    login_btn.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)

    signup_btn = customtkinter.CTkButton(master=frame, width=180, text="Sign Up",
                                         command=lambda: open_signup_window(login))
    signup_btn.place(relx=0.5, rely=0.88, anchor=tkinter.CENTER)

    login.mainloop()