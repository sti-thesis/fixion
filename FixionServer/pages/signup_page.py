import customtkinter
import tkinter
from tkinter import messagebox
import re
import random
import smtplib
from email.message import EmailMessage
import os
from PIL import Image


def center_window(window, width, height):
    """Centers a tkinter window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Global variable to store the generated verification code
verification_code = None

def send_verification_email(email):
    """Send verification email with actual SMTP"""
    global verification_code

    try:
        # Generate 6-digit verification code
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # SMTP setup
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        from_mail = 'sti.fixion@gmail.com'

        server.login(from_mail, 'mxmo zftr ccbw uyhd')

        # Create message
        msg = EmailMessage()
        msg['Subject'] = "Email Verification - OTP Code"
        msg['From'] = from_mail
        msg['To'] = email  # This should be the email string, not the entry widget
        msg.set_content(f"Your verification code is: {verification_code}\n\nThis code will expire in 10 minutes.")

        # Send message
        server.send_message(msg)
        server.quit()

        print(f"Verification email sent to {email} with code: {verification_code}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def open_signup_page(current_window):
    current_window.withdraw()

    # Apply same theme as login page
    signup = customtkinter.CTkToplevel(fg_color="#15141b")
    signup.title("Sign Up Page")

    # Set dimensions and center the window
    width, height = 700, 850
    center_window(signup, width, height)

    # Variables for verification
    email_verified = False

    def check_email_for_send_button():
        """Enable/disable send button based on email validity"""
        email = email_entry.get()
        if email and validate_email(email):
            send_code_btn.configure(state="normal")
        else:
            send_code_btn.configure(state="disabled")

    def send_verification_code():
        """Send verification code to email"""
        nonlocal email_verified
        email = email_entry.get()

        if not email:
            messagebox.showerror("Error", "Please enter an email address!")
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        # Disable the send button while processing
        send_code_btn.configure(state="disabled", text="Sending...")
        signup.update()

        if send_verification_email(email):
            messagebox.showinfo("Code Sent", f"Verification code sent to {email}!")
            send_code_btn.configure(text="Resend", state="normal")
            email_verified = False
            verify_status_label.configure(text="Code sent! Enter code and click Verify", text_color="#e9e8e8")
        else:
            messagebox.showerror("Error",
                                 "Failed to send verification email. Please check your internet connection and try again.")
            send_code_btn.configure(text="Send Code", state="normal")

    def verify_email_code():
        """Verify the entered code"""
        global verification_code
        nonlocal email_verified

        entered_code = verification_entry.get()

        if not entered_code:
            messagebox.showerror("Error", "Please enter the verification code!")
            return

        if not verification_code:
            messagebox.showerror("Error", "Please request a verification code first!")
            return

        # Check if the entered code matches the sent code
        if entered_code == verification_code:
            email_verified = True
            verify_status_label.configure(text="✓ Email Verified", text_color="#047eaf")
            verify_code_btn.configure(state="disabled")
            verification_entry.configure(state="disabled")
            send_code_btn.configure(state="disabled")
            messagebox.showinfo("Success", "Email verified successfully!")
        else:
            messagebox.showerror("Error", "Invalid verification code! Please try again.")

    def process_signup():
        first_name = firstname_entry.get()
        last_name = lastname_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = password2_entry.get()
        role = role_dropdown.get()

        # validation
        if not all([first_name, last_name, email, username, password, confirm_password, role]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        if not email_verified:
            messagebox.showerror("Error", "Please verify your email address first!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return

        if role == "Select Role":
            messagebox.showerror("Error", "Please select a role!")
            return

        if not check_box.get():
            messagebox.showerror("Error", "You must agree to the Terms of Service and Privacy Policy!")
            return

        # Create account
        signup_data = {
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}",
            'email': email,
            'username': username,
            'password': password,  # In real app, hash this password
            'role': role
        }

        print(f"User data: {signup_data}")
        messagebox.showinfo("Success", f"Account created successfully for {username}!")
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

    # Main frame with login theme colors
    frame = customtkinter.CTkFrame(master=signup, width=500, height=780, corner_radius=18, fg_color="#122a3e")
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Title label with login theme styling
    label_1 = customtkinter.CTkLabel(
        master=frame,
        fg_color="transparent",
        text="Create your Account",
        text_color="#e9e8e8",
        font=("Roboto Medium", 20, "bold")
    )
    label_1.place(relx=0.5, rely=0.06, anchor=tkinter.CENTER)

    # Logo

    logo_path = os.path.join(os.path.dirname(__file__), "logo", "fixion_logo.png")
    logo_img = customtkinter.CTkImage(
            light_image=Image.open(logo_path),
            size=(120, 120)
        )

    logo_label = customtkinter.CTkLabel(
        master=frame,
        image=logo_img,
        text=""
        )
    logo_label.place(relx=0.5, rely=0.17, anchor=tkinter.CENTER)


    # Create a frame to hold the first name and last name entries
    name_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent", border_width=0)
    name_frame.place(relx=0.5, rely=0.30, anchor=tkinter.CENTER)

    # First name entry with login theme
    firstname_entry = customtkinter.CTkEntry(
        master=name_frame,
        width=145,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='First Name'
    )
    firstname_entry.grid(row=0, column=0, padx=(0, 5))

    # Last name entry with login theme
    lastname_entry = customtkinter.CTkEntry(
        master=name_frame,
        width=145,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Last Name'
    )
    lastname_entry.grid(row=0, column=1, padx=(5, 0))

    # Email entry with login theme
    email_entry = customtkinter.CTkEntry(
        master=frame,
        width=300,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Email Address'
    )
    email_entry.place(relx=0.5, rely=0.37, anchor=tkinter.CENTER)

    # Bind email entry to enable/disable send button
    email_entry.bind('<KeyRelease>', lambda e: check_email_for_send_button())

    # Verification frame (always shown)
    verification_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent", border_width=0)
    verification_frame.place(relx=0.5, rely=0.44, anchor=tkinter.CENTER)

    # Send code button with login theme
    send_code_btn = customtkinter.CTkButton(
        master=verification_frame,
        width=80,
        corner_radius=12,
        text_color="#e9e8e8",
        fg_color="#047eaf",
        hover_color="#22222f",
        text="Send Code",
        command=send_verification_code,
        state="disabled"
    )
    send_code_btn.grid(row=0, column=0, padx=(0, 5))

    # Verification code entry with login theme
    verification_entry = customtkinter.CTkEntry(
        master=verification_frame,
        width=130,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='6-digit code'
    )
    verification_entry.grid(row=0, column=1, padx=(5, 5))

    # Verify code button with login theme
    verify_code_btn = customtkinter.CTkButton(
        master=verification_frame,
        width=70,
        corner_radius=12,
        text_color="#e9e8e8",
        fg_color="#047eaf",
        hover_color="#22222f",
        text="Verify",
        command=verify_email_code
    )
    verify_code_btn.grid(row=0, column=2, padx=(5, 0))

    # Verification status label with login theme
    verify_status_label = customtkinter.CTkLabel(
        master=frame,
        text="Enter email to enable verification",
        fg_color="transparent",
        text_color="#e9e8e8",
        font=("Roboto Medium", 12)
    )
    verify_status_label.place(relx=0.5, rely=0.48, anchor=tkinter.CENTER)

    # Username entry with login theme
    username_entry = customtkinter.CTkEntry(
        master=frame,
        width=300,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Username'
    )
    username_entry.place(relx=0.5, rely=0.53, anchor=tkinter.CENTER)

    # Password entry with login theme
    password_entry = customtkinter.CTkEntry(
        master=frame,
        width=300,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Password (min 6 characters)',
        show="*"
    )
    password_entry.place(relx=0.5, rely=0.60, anchor=tkinter.CENTER)

    # Confirm password entry with login theme
    password2_entry = customtkinter.CTkEntry(
        master=frame,
        width=300,
        corner_radius=12,
        border_width=0,
        fg_color="#22222f",
        font=("Roboto Medium", 14),
        text_color="#e9e8e8",
        placeholder_text='Confirm Password',
        show="*"
    )
    password2_entry.place(relx=0.5, rely=0.67, anchor=tkinter.CENTER)

    # Role selection dropdown with login theme
    role_dropdown = customtkinter.CTkOptionMenu(
        master=frame,
        width=300,
        corner_radius=12,
        fg_color="#22222f",
        button_color="#047eaf",
        button_hover_color="#22222f",
        dropdown_fg_color="#22222f",
        text_color="#e9e8e8",
        font=("Roboto Medium", 14),
        values=["Admin", "IT Staff", "Developer"]
    )
    role_dropdown.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)
    role_dropdown.set("Select Role")  # Default text

    # Terms checkbox with login theme
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
        font=("Roboto Medium", 12),
        text="I agree to the Terms of Service and Privacy Policy"
    )
    check_box.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)

    # Sign up button with login theme
    signup_btn = customtkinter.CTkButton(
        master=frame,
        width=180,
        corner_radius=12,
        text_color="#e9e8e8",
        fg_color="#047eaf",
        hover_color="#22222f",
        font=("Roboto Medium", 14, "bold"),
        text="Sign Up",
        command=process_signup
    )
    signup_btn.place(relx=0.5, rely=0.86, anchor=tkinter.CENTER)

    # Login button with login theme
    login_btn = customtkinter.CTkButton(
        master=frame,
        width=180,
        corner_radius=12,
        text_color="#e9e8e8",
        fg_color="#047eaf",
        hover_color="#22222f",
        font=("Roboto Medium", 14),
        text="Already Have an Account? Login",
        command=back_to_login
    )
    login_btn.place(relx=0.5, rely=0.93, anchor=tkinter.CENTER)

    signup.protocol("WM_DELETE_WINDOW", back_to_login)
    signup.mainloop()


if __name__ == "__main__":
    # testing lang para sa signup
    root = customtkinter.CTk()
    root.withdraw()
    open_signup_page(root)