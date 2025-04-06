import customtkinter
import tkinter
from tkinter import messagebox


def open_signup_window(current_window):
    current_window.withdraw()

    signup = customtkinter.CTk()
    signup.geometry("500x650")
    signup.title("Signup Page")

    def process_signup():
        full_name = fullname_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = password2_entry.get()

        #validation
        if not all([full_name, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        if not check_box.get():
            messagebox.showerror("Error", "You must agree to the Terms of Service and Privacy Policy!")
            return
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

    frame = customtkinter.CTkFrame(master=signup, width=400, height=550, corner_radius=18)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    logo = customtkinter.CTkFrame(master=frame, width=150, height=150)
    logo.place(relx=0.5, rely=0.21, anchor=tkinter.CENTER)

    label_1 = customtkinter.CTkLabel(master=frame, fg_color="transparent", text="Create an Admin Account")
    label_1.place(relx=0.5, rely=0.39, anchor=tkinter.CENTER)

    fullname_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",placeholder_text='Full Name')
    fullname_entry.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    username_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",placeholder_text='Username')
    username_entry.place(relx=0.5, rely=0.53, anchor=tkinter.CENTER)

    password_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",placeholder_text='Password', show="*")
    password_entry.place(relx=0.5, rely=0.61, anchor=tkinter.CENTER)

    password2_entry = customtkinter.CTkEntry(master=frame, width=300, fg_color="transparent",placeholder_text='Confirm Password', show="*")
    password2_entry.place(relx=0.5, rely=0.69, anchor=tkinter.CENTER)

    check_box = customtkinter.CTkCheckBox(master=frame, checkbox_height=20, checkbox_width=20, border_width=2,text="I agree to the Terms of Service and Privacy Policy")
    check_box.place(relx=0.5, rely=0.76, anchor=tkinter.CENTER)

    signup_btn = customtkinter.CTkButton(master=frame, width=230, text="Sign Up", command=process_signup)
    signup_btn.place(relx=0.5, rely=0.83, anchor=tkinter.CENTER)

    login_btn = customtkinter.CTkButton(master=frame, width=230, text="Already Have an Account? Login", border_width=2,fg_color="transparent", text_color="#ECEFF1", command=back_to_login)
    login_btn.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    signup.protocol("WM_DELETE_WINDOW", back_to_login)
    signup.mainloop()


if __name__ == "__main__":
    # testing lang para sa signup
    root = customtkinter.CTk()
    root.withdraw()
    open_signup_window(root)