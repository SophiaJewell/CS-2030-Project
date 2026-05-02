"""
main.py

Controller layer - Main application entry point

Manages the Tkinter GUI window
handles navigation between screens
"""
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

from session_manager import SessionManager

from security import *
from validator import *
from database_handler import *
from student import *

# Colors
BG_COLOR   = "#dbeafe"
DARK_BG    = "#102030"
CARD_COLOR = "#cbdaee"
DARK_CARD = "#1a3045"

ACCENT     = "#1e3a8a"
TEXT_COLOR = "#111111"
DARK_TEXT = "#eaeaea"

TITLE_COLOR      = "#1e3a8a"
DARK_TITLE_COLOR = "#eaeaea"

ENTRY_BG   = "#fbfafe"
DARK_ENTRY = "#0d1b2a"

BTN_FG            = "#ffffff"
MAIN_BTN_BG_CLICK = "#152a6e"
SEC_BTN_BG        = "#374151"
SEC_BTN_BG_CLICK  = "#4b5563"
BTN_RED           = "#C04030"


STATUS_BG = "#001525"
GREEN     = "#22c55e"
RED       = "#ef4444"

# Fonts
FONT_TITLE  = ("Arial", 28, "bold")
FONT_HEADER = ("Arial", 14, "bold")
FONT_NORMAL = ("Arial", 11)
FONT_SMALL  = ("Arial", 9)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SecureStudentApp:

    def __init__(self):
        # Main window setup
        self.root = tk.Tk()
        self.root.title("Secure Student Management System")
        self.root.geometry("1000x700")
        self.root.minsize(750, 700)
        self.root.resizable(True, True)
        self.root.configure(bg=BG_COLOR)

        # Create the session manager
        self.session = SessionManager()

        # Tracks whether dark mode is on or off
        self.dark_mode = False

        # Mule images
        self.ucm_logo_img = tk.PhotoImage(file="Images/ucm_logo.png")
        self.mule_img = tk.PhotoImage(file="Images/mule.png")

        # Container that holds all screens stacked on top of each other
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Store all screens in a dictionary
        self.frames = {}
        for ScreenClass in (WelcomeFrame, LoginFrame, RegisterFrame, DashboardFrame,
                            ViewAllStudentsFrame, ViewMyRecordFrame,
                            EditStudentFrame, GradesFrame):
            frame = ScreenClass(container, self)
            self.frames[ScreenClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Status bar at the bottom of the window
        self.status_var = tk.StringVar(value="Welcome!")
        self.status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            bg=STATUS_BG, fg=GREEN,
            anchor="w", relief="sunken",
            bd=2, padx=10, font=FONT_SMALL
        )
        self.status_bar.pack(side="bottom", fill="x")

        # Load toggle images
        self.toggle_on_img = tk.PhotoImage(file="Images/toggle_on.png")
        self.toggle_off_img = tk.PhotoImage(file="Images/toggle_off.png")

        # Dark mode toggle button - always visible in top right
        self.theme_btn = tk.Button(
            self.root, image=self.toggle_off_img,
            bg=BG_COLOR, bd=0,
            activebackground=BG_COLOR,
            cursor="hand2",
            command=self.toggle_dark_mode
        )
        self.theme_btn.place(relx=1.0, rely=1.0, anchor="ne", x=-20, y=-90)

        # Show the welcome screen first
        self.show_frame(WelcomeFrame)

    def show_frame(self, frame_class):
        # Brings the requested screen to the front
        frame = self.frames[frame_class]
        frame.tkraise()

        # Reset the screen if it has an on_show method
        if hasattr(frame, "on_show"):
            frame.on_show()

    def set_status(self, msg, ok=True):
        # Updates the status bar text and color
        self.status_var.set(msg)
        self.status_bar.config(fg=GREEN if ok else RED)

    def toggle_dark_mode(self):
        # Flip the dark mode flag
        self.dark_mode = not self.dark_mode

        # Pick the right colors based on mode
        bg = DARK_BG if self.dark_mode else BG_COLOR
        card = DARK_CARD if self.dark_mode else CARD_COLOR
        text = DARK_TEXT if self.dark_mode else TEXT_COLOR
        entry = DARK_ENTRY if self.dark_mode else ENTRY_BG

        # Swap the toggle image
        self.theme_btn.configure(
            image=self.toggle_on_img if self.dark_mode else self.toggle_off_img,
            bg=bg, activebackground=bg
        )

        # Update the main window and status bar
        self.root.configure(bg=bg)
        self.status_bar.configure(bg=STATUS_BG)

        # Tell each frame to update its colors
        for frame in self.frames.values():
            if hasattr(frame, "apply_theme"):
                frame.apply_theme(bg, card, text, entry)

    # Apply new colors after hitting the dark mode button
    def apply_colors(self, frame, bg, card, text, entry):
        # Get all widgets in the frame and its children
        all_widgets = []
        def collect(widget):
            for child in widget.winfo_children():
                all_widgets.append(child)
                collect(child)
        collect(frame)

        # Update each widget's colors
        for child in all_widgets:
            widget_type = child.winfo_class()

            if widget_type == "Frame":
                current_bg = child.cget("bg")
                if current_bg in (CARD_COLOR, DARK_CARD):
                    child.configure(bg=card)
                else:
                    child.configure(bg=bg)
            elif widget_type == "Label":
                current_bg = child.cget("bg")
                current_fg = child.cget("fg")
                if current_bg in (CARD_COLOR, DARK_CARD):
                    child.configure(bg=card, fg=text)
                elif current_fg in (TITLE_COLOR, DARK_TITLE_COLOR):
                    child.configure(bg=bg, fg=DARK_TITLE_COLOR if self.dark_mode else TITLE_COLOR)
                else:
                    child.configure(bg=bg, fg=text)
            elif widget_type == "Entry":
                child.configure(bg=entry, fg=text)

    def run(self):
        self.root.mainloop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Opening page to the program

class WelcomeFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.build()

    def build(self):

        # Ucm Logo label for the bottom center (Extra piece #1)
        logo = self.app.ucm_logo_img.subsample(2)
        logo_label = tk.Label(self, image=logo, bg=BG_COLOR)
        logo_label.image = logo  # Causes image to not disappear
        logo_label.pack(pady=(40, 10))

        # Student Management System Title
        self.title_label = tk.Label(self, text="Student Management System",
                                    bg=BG_COLOR, fg=TITLE_COLOR,
                                    font=FONT_TITLE)
        self.title_label.pack(pady=(0, 60))

        # Register Button
        tk.Button(self, text="Register",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  command=lambda: self.app.show_frame(RegisterFrame),
                  width=24, font=FONT_HEADER, relief="raised",
                  cursor="hand2", activeforeground=BTN_FG).pack(pady=10, ipady=6)

        # Login Button
        tk.Button(self, text="Login",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  command=lambda: self.app.show_frame(LoginFrame),
                  width=24, font=FONT_HEADER, relief="raised",
                  cursor="hand2", activeforeground=BTN_FG).pack(pady=10, ipady=6)

        # Exit Button
        tk.Button(self, text="Exit",
                  bg=SEC_BTN_BG, fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  command=self.app.root.quit,
                  width=24, font=FONT_HEADER, relief="raised",
                  cursor="hand2", activeforeground=BTN_FG).pack(pady=10, ipady=6)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Login page for user to login to account

class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.build()

    def build(self):
        tk.Label(self, text="Login",
                 bg=BG_COLOR, fg=TITLE_COLOR,
                 font=FONT_TITLE).pack(pady=(60, 20))

        card = tk.Frame(self, bg=CARD_COLOR, bd=1, relief="groove")
        card.pack(pady=10, padx=150)

        # Email field
        tk.Label(card, text="Email:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(20, 2))

        self.email_var = tk.StringVar()
        tk.Entry(card, textvariable=self.email_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 20), ipady=6)

        # Password field
        tk.Label(card, text="Password:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))

        self.pw_var = tk.StringVar()
        tk.Entry(card, textvariable=self.pw_var, show="*",
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 20), ipady=6)

        # Shows remaining attempts when login fails
        self.attempt_label = tk.Label(card, text="", bg=CARD_COLOR,
                                      fg=RED, font=FONT_SMALL)
        self.attempt_label.pack(pady=(0, 4))

        # Buttons
        btn_row = tk.Frame(card, bg=CARD_COLOR)
        btn_row.pack(pady=24)

        # Login Button
        tk.Button(btn_row, text="Login",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_HEADER, width=12, cursor="hand2",
                  command=self.attempt_login).pack(side="left", padx=8, ipady=6)

        # Back Button
        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG , fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=8, cursor="hand2",
                  command=self.go_back).pack(side="left", padx=8, ipady=10)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)

    def on_show(self):
        # Reset the form when screen is navigated to
        self.email_var.set("")
        self.pw_var.set("")
        self.attempt_label.config(text="")
        self.app.session.reset_attempts()
        self.app.set_status("Enter your credentials to log in.")

    def attempt_login(self):
        email = self.email_var.get().strip()
        password = self.pw_var.get().strip()

        # Check if fields are empty
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if already locked out
        if self.app.session.is_locked_out():
            messagebox.showerror("Locked Out", "Too many failed attempts.")
            self.go_back()
            return

        # Look up the user in the database and verify their password
        user = find_user_by_email(email)
        success = user is not None and verify_password(password, user["password"])

        if success:
            self.app.session.login(email, role=user["role"])
            self.app.set_status(f"Welcome, {email}!", ok=True)
            self.app.show_frame(DashboardFrame)
        else:
            self.app.session.record_failed_attempt()
            remaining = self.app.session.attempts_remaining()
            self.attempt_label.config(text=f"Invalid credentials. {remaining} attempt(s) left.")
            self.app.set_status("Login failed.", ok=False)

            if self.app.session.is_locked_out():
                messagebox.showerror("Locked Out", "Maximum attempts reached.")
                self.go_back()

    def go_back(self):
        self.app.session.reset_attempts()
        self.app.show_frame(WelcomeFrame)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Register page to create users account

class RegisterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.build()

    def build(self):
        tk.Label(self, text="Register",
                 bg=BG_COLOR, fg=TITLE_COLOR,
                 font=FONT_TITLE).pack(pady=(40, 20))

        # Frame to put info inside of
        card = tk.Frame(self, bg=CARD_COLOR, bd=1, relief="groove")
        card.pack(pady=10, padx=80)

        # Left column - Account info
        left = tk.Frame(card, bg=CARD_COLOR)
        left.grid(row=0, column=0, padx=24, pady=20, sticky="n")

        # Email Entry
        tk.Label(left, text="Email:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.email_var = tk.StringVar()
        tk.Entry(left, textvariable=self.email_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Student ID Entry
        tk.Label(left, text="Student ID:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.student_id_var = tk.StringVar()
        tk.Entry(left, textvariable=self.student_id_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Password Entry
        tk.Label(left, text="Password:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.pw_var = tk.StringVar()
        tk.Entry(left, textvariable=self.pw_var, show="*",
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Password Confirm Entry
        tk.Label(left, text="Confirm Password:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.cpw_var = tk.StringVar()
        tk.Entry(left, textvariable=self.cpw_var, show="*",
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Right column - Student info
        right = tk.Frame(card, bg=CARD_COLOR)
        right.grid(row=0, column=1, padx=24, pady=20, sticky="n")

        # First Name Entry
        tk.Label(right, text="First Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.first_var = tk.StringVar()
        tk.Entry(right, textvariable=self.first_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Last Name Entry
        tk.Label(right, text="Last Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.last_var = tk.StringVar()
        tk.Entry(right, textvariable=self.last_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Age Entry
        tk.Label(right, text="Age (16-100):", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.age_var = tk.StringVar()
        tk.Entry(right, textvariable=self.age_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Gender Entry
        tk.Label(right, text="Gender:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.gender_var = tk.StringVar(value="Male")
        tk.OptionMenu(right, self.gender_var, "Male", "Female", "Other").pack(
            anchor="w", pady=(0, 12))

        # Phone entry
        tk.Label(right, text="Phone (xxx-xxx-xxxx):", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", pady=(0, 2))
        self.phone_var = tk.StringVar()
        tk.Entry(right, textvariable=self.phone_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=28
                 ).pack(anchor="w", pady=(0, 12), ipady=6)

        # Row for buttons
        btn_row = tk.Frame(card, bg=CARD_COLOR)
        btn_row.grid(row=1, column=0, columnspan=2, pady=16)

        # Register button
        tk.Button(btn_row, text="Register",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_HEADER, width=12, cursor="hand2",
                  command=self.attempt_register).pack(side="left", padx=8, ipady=6)

        # Back button
        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG, fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=8, cursor="hand2",
                  command=self.go_back).pack(side="left", padx=8, ipady=10)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)

    # Reset textboxes on show
    def on_show(self):
        self.email_var.set("")
        self.student_id_var.set("")
        self.first_var.set("")
        self.last_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        self.phone_var.set("")
        self.pw_var.set("")
        self.cpw_var.set("")
        self.app.set_status("Fill in the form to create an account.")

    # Strip and attemp to register. If fail, give error message
    def attempt_register(self):
        email      = self.email_var.get().strip()
        student_id = self.student_id_var.get().strip()
        first      = self.first_var.get().strip()
        last       = self.last_var.get().strip()
        age        = self.age_var.get().strip()
        gender     = self.gender_var.get().strip()
        phone      = self.phone_var.get().strip()
        pw         = self.pw_var.get().strip()
        confirm    = self.cpw_var.get().strip()

        # Check if fields are empty
        if not email or not student_id or not first or not last or not age or not phone or not pw or not confirm:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Check if passwords match
        if pw != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Validate email
        email_ok, email_msg = validate_email(email)
        if not email_ok:
            messagebox.showerror("Error", email_msg)
            return

        # Validate student ID
        id_ok, id_msg = validate_student_id(student_id)
        if not id_ok:
            messagebox.showerror("Error", id_msg)
            return

        # Check if student ID is already linked to another account
        for user in get_users():
            if user.get("student_id") == student_id:
                messagebox.showerror("Error", "That Student ID is already linked to an account.")
                return

        # Validate name
        first_ok, first_msg = validate_name(first)
        if not first_ok:
            messagebox.showerror("Error", first_msg)
            return

        last_ok, last_msg = validate_name(last)
        if not last_ok:
            messagebox.showerror("Error", last_msg)
            return

        # Validate age
        age_ok, age_msg = validate_age(age)
        if not age_ok:
            messagebox.showerror("Error", age_msg)
            return

        # Validate phone
        phone_ok, phone_msg = validate_phone(phone)
        if not phone_ok:
            messagebox.showerror("Error", phone_msg)
            return

        # Validate password
        pw_ok, pw_msg = validate_password(pw)
        if not pw_ok:
            messagebox.showerror("Error", pw_msg)
            return

        # Save user account and student record
        try:
            add_user({
                "email": email,
                "password": hash_password(pw),
                "role": "user",
                "student_id": student_id
            })
            add_student({
                "student_id": student_id,
                "first_name": first,
                "last_name":  last,
                "age":        int(age),
                "gender":     gender,
                "phone":      phone
            })
            self.app.set_status(f"Account created for {email}!", ok=True)
            messagebox.showinfo("Registered", f"Account created!\nEmail: {email}")
            if self.app.session.is_logged_in():
                self.app.show_frame(DashboardFrame)
            else:
                self.app.show_frame(WelcomeFrame)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        if self.app.session.is_logged_in():
            self.app.show_frame(DashboardFrame)
        else:
            self.app.show_frame(WelcomeFrame)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Dashboard frame

class DashboardFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.current_bg = BG_COLOR
        self.current_card = CARD_COLOR
        self.current_text = TEXT_COLOR
        self.current_entry = ENTRY_BG

    def on_show(self):
        # Rebuild dashboard when shown
        for widget in self.winfo_children():
            widget.destroy()
        self.build()

    def build(self):
        # Get users role to show different buttons
        role = self.app.session.get_current_role()
        email = self.app.session.get_current_email()

        # Welcome message
        self.title_label = tk.Label(self, text=f"Welcome, {email}!",
                                    bg=self.current_bg, fg=TITLE_COLOR,
                                    font=FONT_TITLE)
        self.title_label.pack(pady=(60, 4))

        tk.Label(self, text=f"Logged in as: {role}",
                 bg=self.current_bg, fg=self.current_text,
                 font=FONT_NORMAL).pack(pady=(0, 30))

        # If role "admin" Show View all Students and Add Student Option
        if role == "admin":
            # View All Students Button
            tk.Button(self, text="View All Students",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self.view_all_students).pack(pady=10, ipady=6)

            # Add student button
            tk.Button(self, text="Add Student",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self.add_student).pack(pady=10, ipady=6)
        # Else (student), show View My Record and View My Grades
        else:
            # View My Record button
            tk.Button(self, text="View My Record",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self.view_my_record).pack(pady=10, ipady=6)

            # View My Grades button
            tk.Button(self, text="View My Grades",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self.view_my_grades).pack(pady=10, ipady=6)

        # Logout button
        tk.Button(self, text="Logout",
                  bg=SEC_BTN_BG, fg=BTN_FG,
                  activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_HEADER, width=24, cursor="hand2",
                  command=self.logout).pack(pady=10, ipady=6)

    def view_all_students(self):
        self.app.show_frame(ViewAllStudentsFrame)

    def add_student(self):
        self.app.show_frame(RegisterFrame)

    def view_my_record(self):
        self.app.show_frame(ViewMyRecordFrame)

    # Bring user to their grade
    def view_my_grades(self):
        email = self.app.session.get_current_email()
        user = find_user_by_email(email)
        student_id = user.get("student_id", "")
        self.app.frames[GradesFrame].load_student(student_id, role="user")
        self.app.show_frame(GradesFrame)

    def logout(self):
        self.app.session.logout()
        self.app.set_status("Logged out successfully.")
        self.app.show_frame(WelcomeFrame)

    def apply_theme(self, bg, card, text, entry):
        self.current_bg = bg
        self.current_card = card
        self.current_text = text
        self.current_entry = entry
        self.configure(bg=bg)
        for widget in self.winfo_children():
            widget.destroy()
        self.build()
        self.app.apply_colors(self, bg, card, text, entry)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ViewAllStudentsFrame

class ViewAllStudentsFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.build()

    def build(self):
        tk.Label(self, text="All Students",
                 bg=BG_COLOR, fg=TITLE_COLOR,
                 font=FONT_TITLE).pack(pady=(30, 10))

        # Table container
        table_frame = tk.Frame(self, bg=BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Table style
        style = ttk.Style()
        style.theme_use("winnative")
        style.configure("Treeview",
                        background=CARD_COLOR,
                        foreground=TEXT_COLOR,
                        fieldbackground=CARD_COLOR,
                        rowheight=28,
                        font=FONT_NORMAL)
        style.configure("Treeview.Heading",
                        background=ACCENT,
                        foreground=BTN_FG,
                        font=FONT_HEADER,
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", MAIN_BTN_BG_CLICK)],
                  foreground=[("selected", BTN_FG)])
        style.configure("Vertical.TScrollbar",
                        background=CARD_COLOR,
                        troughcolor=BG_COLOR)


        self.tree = ttk.Treeview(table_frame,
                                  columns=("id", "first", "last", "age", "gender", "phone"),
                                  show="headings", height=16)

        # Define column headings and widths
        self.tree.heading("id", text="Student ID", anchor="w")
        self.tree.heading("first", text="First Name", anchor="w")
        self.tree.heading("last", text="Last Name", anchor="w")
        self.tree.heading("age", text="Age", anchor="w")
        self.tree.heading("gender", text="Gender", anchor="w")
        self.tree.heading("phone", text="Phone", anchor="w")

        self.tree.column("id", width=80)
        self.tree.column("first", width=80)
        self.tree.column("last", width=80)
        self.tree.column("age", width=30)
        self.tree.column("gender", width=50)
        self.tree.column("phone", width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Button row
        btn_row = tk.Frame(self, bg=BG_COLOR)
        btn_row.pack(pady=14)

        # View Grades Button
        tk.Button(btn_row, text="View Grades",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=14, cursor="hand2",
                  command=self.view_grades).pack(side="left", padx=8, ipady=6)

        # Edit Student Button
        tk.Button(btn_row, text="Edit Student",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=16, cursor="hand2",
                  command=self.edit_student).pack(side="left", padx=8, ipady=6)

        # Delete Student Button
        tk.Button(btn_row, text="Delete Student",
                  bg=RED, fg=BTN_FG, activebackground=BTN_RED,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=16, cursor="hand2",
                  command=self.delete_student).pack(side="left", padx=8, ipady=6)

        # Back button
        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG, fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=12, cursor="hand2",
                  command=self.go_back).pack(side="left", padx=8, ipady=6)

    def delete_student(self):
        # Get selected row
        selected = self.tree.selection()

        # Error if no student selected
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete.")
            return

        # Get the student ID from the selected row
        student_id = self.tree.item(selected[0], "values")[0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete student {student_id}?")
        if not confirm:
            return

        try:
            delete_student(student_id)
            self.app.set_status(f"Student {student_id} deleted.", ok=True)
            self.on_show()  # Refresh the table
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Clear and reload the table on show
    def on_show(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = get_students()

        if not students:
            self.app.set_status("No students found.", ok=False)
            return

        for student in students:
            self.tree.insert("", "end", values=(
                student.get("student_id", ""),
                student.get("first_name", ""),
                student.get("last_name", ""),
                student.get("age", ""),
                student.get("gender", ""),
                student.get("phone", "")
            ))

        self.app.set_status(f"{len(students)} student(s) found.")

    def go_back(self):
        self.app.show_frame(DashboardFrame)

    def view_grades(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to view grades.")
            return
        student_id = self.tree.item(selected[0], "values")[0]
        self.app.frames[GradesFrame].load_student(student_id)
        self.app.show_frame(GradesFrame)

    def edit_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to edit.")
            return
        student_id = self.tree.item(selected[0], "values")[0]
        self.app.frames[EditStudentFrame].load_student(student_id)
        self.app.show_frame(EditStudentFrame)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)
        style = ttk.Style()
        style.configure("Treeview",
                        background=card,
                        foreground=text,
                        fieldbackground=card)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# EditStudentFrame

class EditStudentFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.student_id = None
        self.build()

    def build(self):
        tk.Label(self, text="Edit Student",
                 bg=BG_COLOR, fg=TITLE_COLOR,
                 font=FONT_TITLE).pack(pady=(40, 20))

        # Frame to keep text fields in
        card = tk.Frame(self, bg=CARD_COLOR, bd=1, relief="groove")
        card.pack(pady=10, padx=150)

        # First name field
        tk.Label(card, text="First Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(20, 2))
        self.first_var = tk.StringVar()
        tk.Entry(card, textvariable=self.first_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 12), ipady=6)

        # Last name field
        tk.Label(card, text="Last Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))
        self.last_var = tk.StringVar()
        tk.Entry(card, textvariable=self.last_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 12), ipady=6)

        # Age field
        tk.Label(card, text="Age (16-100):", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))
        self.age_var = tk.StringVar()
        tk.Entry(card, textvariable=self.age_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 12), ipady=6)

        # Gender field
        tk.Label(card, text="Gender:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))
        self.gender_var = tk.StringVar(value="Male")

        tk.OptionMenu(card, self.gender_var, "Male", "Female", "Other").pack(
            anchor="w", padx=24, pady=(0, 12))

        # Phone field
        tk.Label(card, text="Phone xxx-xxx-xxxx:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))
        self.phone_var = tk.StringVar()
        tk.Entry(card, textvariable=self.phone_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 12), ipady=6)

        # Buttons
        btn_row = tk.Frame(card, bg=CARD_COLOR)
        btn_row.pack(pady=24)

        tk.Button(btn_row, text="Save Changes",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_HEADER, width=12, cursor="hand2",
                  command=self.submit).pack(side="left", padx=8, ipady=6)

        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG, fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=8, cursor="hand2",
                  command=self.go_back).pack(side="left", padx=8, ipady=10)

    # Load the student's current data into the fields
    def load_student(self, student_id):
        self.student_id = student_id
        student = find_student_by_id(student_id)

        self.first_var.set(student.get("first_name", ""))
        self.last_var.set(student.get("last_name", ""))
        self.age_var.set(str(student.get("age", "")))
        self.gender_var.set(student.get("gender", "Male"))
        self.phone_var.set(student.get("phone", ""))

        self.app.set_status(f"Editing student {student_id}.")

    def submit(self):
        first  = self.first_var.get().strip()
        last   = self.last_var.get().strip()
        age    = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        phone  = self.phone_var.get().strip()

        # Check if fields are empty
        if not first or not last or not age or not phone:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate fields
        first_ok, first_msg = validate_name(first)
        if not first_ok:
            messagebox.showerror("Error", first_msg)
            return

        last_ok, last_msg = validate_name(last)
        if not last_ok:
            messagebox.showerror("Error", last_msg)
            return

        age_ok, age_msg = validate_age(age)
        if not age_ok:
            messagebox.showerror("Error", age_msg)
            return

        phone_ok, phone_msg = validate_phone(phone)
        if not phone_ok:
            messagebox.showerror("Error", phone_msg)
            return

        # Save the updated student
        try:
            update_student(self.student_id, {
                "first_name": first,
                "last_name":  last,
                "age":        int(age),
                "gender":     gender,
                "phone":      phone
            })
            self.app.set_status(f"Student {self.student_id} updated!", ok=True)
            messagebox.showinfo("Success", f"Student updated successfully!")
            self.go_back()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.app.show_frame(ViewAllStudentsFrame)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# GradesFrame - FOr Admin to view and manages student grades

class GradesFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.student_id = None
        self.grade_manager = None
        self.build()

    def build(self):
        # TItle label
        self.title_label = tk.Label(self, text="Student Grades",
                 bg=BG_COLOR, fg=TITLE_COLOR,
                 font=FONT_TITLE)
        self.title_label.pack(pady=(30, 10))

        self.id_label = tk.Label(self, text="",
                                 bg=BG_COLOR, fg=TEXT_COLOR,
                                 font=FONT_NORMAL)
        self.id_label.pack(pady=(0, 10))

        # Table container
        table_frame = tk.Frame(self, bg=BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=40, pady=10)

        style = ttk.Style()
        style.theme_use("winnative")

        self.tree = ttk.Treeview(table_frame,
                                  columns=("course", "grades", "average", "letter"),
                                  show="headings", height=10)

        # Headers
        self.tree.heading("course",  text="Course",  anchor="w")
        self.tree.heading("grades",  text="Grades",  anchor="w")
        self.tree.heading("average", text="Average", anchor="w")
        self.tree.heading("letter",  text="Letter",  anchor="w")

        # Columns and size
        self.tree.column("course",  width=150)
        self.tree.column("grades",  width=200)
        self.tree.column("average", width=80)
        self.tree.column("letter",  width=80)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add course/grade section
        # Card to frame name and grage fields
        self.input_card = tk.Frame(self, bg=CARD_COLOR, bd=1, relief="groove")
        self.input_card.pack(padx=40, pady=10)

        # Course name field
        tk.Label(self.input_card, text="Course Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(16, 2))

        self.course_var = tk.StringVar()
        tk.Entry(self.input_card, textvariable=self.course_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 10), ipady=6)

        # Grade field
        tk.Label(self.input_card, text="Grade (0-100):", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))
        self.grade_var = tk.StringVar()

        tk.Entry(self.input_card, textvariable=self.grade_var,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 16), ipady=6)

        # Buttons
        # Frame to store buttons in a row
        btn_row = tk.Frame(self, bg=BG_COLOR)
        btn_row.pack(pady=14)

        # Add Grade button
        self.add_grade_btn = tk.Button(btn_row, text="Add Grade",
                                       bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                                       activeforeground=BTN_FG, relief="raised",
                                       font=FONT_NORMAL, width=14, cursor="hand2",
                                       command=self.add_grade)
        self.add_grade_btn.pack(side="left", padx=8, ipady=6)

        # Delete Grade button
        self.delete_grade_btn = tk.Button(btn_row, text="Delete Grade",
                                          bg=RED, fg=BTN_FG, activebackground=BTN_RED,
                                          activeforeground=BTN_FG, relief="raised",
                                          font=FONT_NORMAL, width=14, cursor="hand2",
                                          command=self.delete_grade)
        self.delete_grade_btn.pack(side="left", padx=8, ipady=6)

        # Delete the course btton
        self.delete_course_btn = tk.Button(btn_row, text="Delete Course",
                                           bg=RED, fg=BTN_FG, activebackground=BTN_RED,
                                           activeforeground=BTN_FG, relief="raised",
                                           font=FONT_NORMAL, width=14, cursor="hand2",
                                           command=self.delete_course)
        self.delete_course_btn.pack(side="left", padx=8, ipady=6)

        # Back button
        self.back_btn = tk.Button(btn_row, text="Back",
                                  bg=SEC_BTN_BG, fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                                  activeforeground=BTN_FG, relief="raised",
                                  font=FONT_NORMAL, width=12, cursor="hand2",
                                  command=self.go_back)
        self.back_btn.pack(side="left", padx=8, ipady=6)

    # Load student grade info
    def load_student(self, student_id, role="admin"):
        self.student_id = student_id
        self.role = role
        student = find_student_by_id(student_id)
        first = student.get("first_name", "")
        last = student.get("last_name", "")

        grades_data = get_grades(student_id)
        self.grade_manager = grademanager.from_dict({
            "student_id": student_id,
            "grades": grades_data
        })
        self.title_label.config(text=f"Grades - {first} {last}")
        self.id_label.config(text=f"Student ID: {student_id}")

        # Forget the buttons, then resort them at the end.
        self.add_grade_btn.pack_forget()
        self.delete_grade_btn.pack_forget()
        self.delete_course_btn.pack_forget()
        self.back_btn.pack_forget()

        # Show or hide admin buttons based on role
        if role == "admin":
            self.input_card.pack(padx=10, pady=10)
            self.add_grade_btn.pack(side="left", padx=8, ipady=6)
            self.delete_grade_btn.pack(side="left", padx=8, ipady=6)
            self.delete_course_btn.pack(side="left", padx=8, ipady=6)
        else:
            self.input_card.pack_forget()

        self.back_btn.pack(side="left", padx=8, ipady=6)

        self.refresh_table()


    def refresh_table(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # fill the table using grademanager
        for row in self.grade_manager.getgrades():
            course = row[0]
            grades = row[1]
            if grades:
                avg = self.grade_manager.calculate_average(course)
                letter = self.grade_manager.convert_to_letter(avg)
                grades_str = ", ".join(str(g) for g in grades)
                self.tree.insert("", "end", values=(course, grades_str, f"{avg:.1f}", letter))
            else:
                self.tree.insert("", "end", values=(course, "No grades yet", "-", "-"))

    # add a grade to a students information
    def add_grade(self):
        course = self.course_var.get().strip()
        grade  = self.grade_var.get().strip()

        if not course or not grade:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        try:
            grade = float(grade)
            if grade < 0 or grade > 100:
                messagebox.showerror("Error", "Grade must be between 0 and 100.")
                return
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number.")
            return

        # Add course if it doesn't exist yet
        existing_courses = [row[0] for row in self.grade_manager.getgrades()]
        if course not in existing_courses:
            self.grade_manager.add_course(course)

        self.grade_manager.add_grade(course, grade)

        # Save to database
        save_grades(self.student_id, self.grade_manager.getgrades())

        self.course_var.set("")
        self.grade_var.set("")
        self.refresh_table()
        self.app.set_status(f"Grade added to {course}.", ok=True)

    # Delete a course from students information
    def delete_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a course to delete.")
            return

        course = self.tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete {course} and all its grades?")
        if not confirm:
            return

        # Remove the course from grade manager
        grades = self.grade_manager.getgrades()
        updated = [row for row in grades if row[0] != course]
        self.grade_manager.setgrades(updated)

        save_grades(self.student_id, self.grade_manager.getgrades())
        self.refresh_table()
        self.app.set_status(f"{course} deleted.", ok=True)

    # Delete a students grade, (Creates a popup to have the user select which grade in the stirng
    def delete_grade(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a course to delete a grade from.")
            return

        course = self.tree.item(selected[0], "values")[0]

        # Get grades for selected course
        grades = []
        for row in self.grade_manager.getgrades():
            if row[0] == course:
                grades = row[1]
                break

        if not grades:
            messagebox.showerror("Error", "This course has no grades to delete.")
            return

        # Create popup
        popup = tk.Toplevel(self.app.root)
        popup.title("Delete Grade")
        popup.geometry("200x250")
        popup.configure(bg=BG_COLOR)
        popup.resizable(False, False)

        tk.Label(popup, text="Select grade to delete:",
                 bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL).pack(pady=(20, 8))

        grade_var = tk.StringVar(value=str(grades[0]))
        grade_options = [str(g) for g in grades]
        tk.OptionMenu(popup, grade_var, *grade_options).pack(pady=(0, 16))

        def confirm_delete():
            selected_grade = float(grade_var.get())
            for row in self.grade_manager.getgrades():
                if row[0] == course:
                    row[1].remove(selected_grade)
                    break
            save_grades(self.student_id, self.grade_manager.getgrades())
            self.refresh_table()
            self.app.set_status(f"Grade removed from {course}.", ok=True)
            popup.destroy()

        # Delete button
        tk.Button(popup, text="Delete",
                  bg=RED, fg=BTN_FG, activebackground=BTN_RED,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, cursor="hand2",
                  command=confirm_delete).pack()

    def go_back(self):
        if self.role == "admin":
            self.app.show_frame(ViewAllStudentsFrame)
        else:
            self.app.show_frame(DashboardFrame)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ViewMyRecordFrame

class ViewMyRecordFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self.build()

    def build(self):
        tk.Label(self, text="My Record",
                 bg=BG_COLOR, fg=TITLE_COLOR,
                 font=FONT_TITLE).pack(pady=(60, 20))

        self.card = tk.Frame(self, bg=CARD_COLOR, bd=1, relief="groove")
        self.card.pack(pady=10, padx=150)

        # Row labels (left column)
        (tk.Label(self.card, text="Student ID:", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
         .grid(row=0, column=0, sticky="w", padx=(24, 10), pady=8))
        (tk.Label(self.card, text="First Name:", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
         .grid(row=1, column=0, sticky="w", padx=(24, 10), pady=8))
        (tk.Label(self.card, text="Last Name:", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
         .grid(row=2, column=0, sticky="w", padx=(24, 10), pady=8))
        (tk.Label(self.card, text="Age:", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
         .grid(row=3, column=0,sticky="w", padx=(24, 10), pady=8))
        (tk.Label(self.card, text="Gender:", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
         .grid(row=4, column=0, sticky="w", padx=(24, 10), pady=8))
        (tk.Label(self.card, text="Phone:", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
         .grid(row=5, column=0, sticky="w", padx=(24, 10), pady=8))

        # Value labels (right column)
        self.id_label = tk.Label(self.card, text="", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
        self.first_label = tk.Label(self.card, text="", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
        self.last_label = tk.Label(self.card, text="", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
        self.age_label = tk.Label(self.card, text="", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
        self.gender_label = tk.Label(self.card, text="", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
        self.phone_label = tk.Label(self.card, text="", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)

        self.id_label.grid(row=0, column=1, sticky="w", padx=(0, 24), pady=8)
        self.first_label.grid(row=1, column=1, sticky="w", padx=(0, 24), pady=8)
        self.last_label.grid(row=2, column=1, sticky="w", padx=(0, 24), pady=8)
        self.age_label.grid(row=3, column=1, sticky="w", padx=(0, 24), pady=8)
        self.gender_label.grid(row=4, column=1, sticky="w", padx=(0, 24), pady=8)
        self.phone_label.grid(row=5, column=1, sticky="w", padx=(0, 24), pady=8)

        # Back button
        tk.Button(self, text="Back",
                  bg=SEC_BTN_BG, fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=12, cursor="hand2",
                  command=self.go_back).pack(pady=20, ipady=6)

    def on_show(self):
        # Clear labels
        self.id_label.config(text="")
        self.first_label.config(text="")
        self.last_label.config(text="")
        self.age_label.config(text="")
        self.gender_label.config(text="")
        self.phone_label.config(text="")

        # Get the logged in user's student ID
        email = self.app.session.get_current_email()
        user = find_user_by_email(email)

        if not user or "student_id" not in user:
            self.app.set_status("No student record linked to this account.", ok=False)
            return

        # Look up the student record
        student = find_student_by_id(user["student_id"])

        if not student:
            self.app.set_status("Student record not found.", ok=False)
            return

        # Update the labels with the student's info
        self.id_label.config(text=student.get('student_id', ''))
        self.first_label.config(text=student.get('first_name', ''))
        self.last_label.config(text=student.get('last_name', ''))
        self.age_label.config(text=str(student.get('age', '')))
        self.gender_label.config(text=student.get('gender', ''))
        self.phone_label.config(text=student.get('phone', ''))

        self.app.set_status(f"Showing record for {email}.")

    def go_back(self):
        self.app.show_frame(DashboardFrame)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app.apply_colors(self, bg, card, text, entry)

if __name__ == "__main__":
    app = SecureStudentApp()
    app.run()