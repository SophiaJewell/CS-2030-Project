"""
main.py

Controller layer - Main application entry point

Manages the Tkinter GUI window
handles navigation between screens
"""
import tkinter as tk
from tkinter import messagebox

from session_manager import SessionManager

from security import hash_password, verify_password
from validator import validate_email, validate_password
from database_handler import find_user_by_email, add_user

# Colors
BG_COLOR   = "#dbeafe"
DARK_BG    = "#102030"
CARD_COLOR = "#cbdaee"
DARK_CARD = "#1a3045"

ACCENT     = "#1e3a8a"
TEXT_COLOR = "#111111"
DARK_TEXT = "#eaeaea"

ENTRY_BG   = "#fbfafe"
DARK_ENTRY = "#0d1b2a"

BTN_FG            = "#ffffff"
MAIN_BTN_BG_CLICK = "#152a6e"
SEC_BTN_BG        = "#374151"
SEC_BTN_BG_CLICK  = "#4b5563"


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
        self.root.geometry("750x600")
        self.root.minsize(600, 550)
        self.root.resizable(True, True)
        self.root.configure(bg=BG_COLOR)

        # Create the session manager
        self.session = SessionManager()

        # Tracks whether dark mode is on or off
        self.dark_mode = False

        # Container that holds all screens stacked on top of each other
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Store all screens in a dictionary
        self.frames = {}
        for ScreenClass in (WelcomeFrame, LoginFrame, RegisterFrame, DashboardFrame):
            frame = ScreenClass(container, self)
            self.frames[ScreenClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Status bar at the bottom of the window
        self.status_var = tk.StringVar(value="Welcome!")
        self._status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            bg=STATUS_BG, fg=GREEN,
            anchor="w", relief="sunken",
            bd=2, padx=10, font=FONT_SMALL
        )
        self._status_bar.pack(side="bottom", fill="x")

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
        self._status_bar.config(fg=GREEN if ok else RED)

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
        self._status_bar.configure(bg=STATUS_BG)

        # Tell each frame to update its colors
        for frame in self.frames.values():
            if hasattr(frame, "apply_theme"):
                frame.apply_theme(bg, card, text, entry)

    # Apply new colors after hitting the dark mode button
    def _apply_colors(self, frame, bg, card, text, entry):
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
                if current_bg in (CARD_COLOR, DARK_CARD):
                    child.configure(bg=card, fg=text)
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
        self._build()

    def _build(self):
        # Student Management System Title
        self.title_label = tk.Label(self, text="Student Management System",
                                    bg=BG_COLOR, fg=ACCENT,
                                    font=FONT_TITLE)
        self.title_label.pack(pady=(140, 60))

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
        self.app._apply_colors(self, bg, card, text, entry)
        title_fg = DARK_TEXT if self.app.dark_mode else ACCENT
        self.title_label.configure(fg=title_fg)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Login page for user to login to account

class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="Login",
                 bg=BG_COLOR, fg=ACCENT,
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
                  command=self._attempt_login).pack(side="left", padx=8, ipady=6)

        # Back Button
        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG , fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=8, cursor="hand2",
                  command=self._go_back).pack(side="left", padx=8, ipady=10)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app._apply_colors(self, bg, card, text, entry)

    def on_show(self):
        # Reset the form when screen is navigated to
        self.email_var.set("")
        self.pw_var.set("")
        self.attempt_label.config(text="")
        self.app.session.reset_attempts()
        self.app.set_status("Enter your credentials to log in.")

    def _attempt_login(self):
        email = self.email_var.get().strip()
        password = self.pw_var.get().strip()

        # Check if fields are empty
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if already locked out
        if self.app.session.is_locked_out():
            messagebox.showerror("Locked Out", "Too many failed attempts.")
            self._go_back()
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
                self._go_back()

    def _go_back(self):
        self.app.session.reset_attempts()
        self.app.show_frame(WelcomeFrame)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Register page to create users account

class RegisterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="Register",
                 bg=BG_COLOR, fg=ACCENT,
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

        # Confirm password field
        tk.Label(card, text="Confirm Password:", bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=FONT_NORMAL).pack(anchor="w", padx=24, pady=(0, 2))
        self.cpw_var = tk.StringVar()

        tk.Entry(card, textvariable=self.cpw_var, show="*",
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="black",
                 relief="flat", font=FONT_NORMAL, width=32
                 ).pack(anchor="w", padx=24, pady=(0, 20), ipady=6)

        # Buttons
        btn_row = tk.Frame(card, bg=CARD_COLOR)
        btn_row.pack(pady=24)

        # Register Button
        tk.Button(btn_row, text="Register",
                  bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_HEADER, width=12, cursor="hand2",
                  command=self._attempt_register).pack(side="left", padx=8, ipady=6)

        # Back button
        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG , fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=8, cursor="hand2",
                  command=self._go_back).pack(side="left", padx=8, ipady=10)

    def apply_theme(self, bg, card, text, entry):
        self.configure(bg=bg)
        self.app._apply_colors(self, bg, card, text, entry)

    def on_show(self):
        # Reset the form when this screen is navigated to
        self.email_var.set("")
        self.pw_var.set("")
        self.cpw_var.set("")
        self.app.set_status("Fill in the form to create an account.")

    def _attempt_register(self):
        email   = self.email_var.get().strip()
        pw      = self.pw_var.get().strip()
        confirm = self.cpw_var.get().strip()

        # Check if fields are empty
        if not email or not pw or not confirm:
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

        # Validate password
        pw_ok, pw_msg = validate_password(pw)
        if not pw_ok:
            messagebox.showerror("Error", pw_msg)
            return

        # Hash the password and save the new user
        try:
            add_user({
                "email": email,
                "password": hash_password(pw),
                "role": "user"
            })
            self.app.set_status(f"Account created for {email}!", ok=True)
            messagebox.showinfo("Registered", f"Account created!\nEmail: {email}")
            self.app.show_frame(WelcomeFrame)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _go_back(self):
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
        self._build()

    def _build(self):
        role = self.app.session.get_current_role()
        email = self.app.session.get_current_email()

        # Welcome message
        self.title_label = tk.Label(self, text=f"Welcome, {email}!",
                                    bg=self.current_bg, fg=ACCENT,
                                    font=FONT_TITLE)
        self.title_label.pack(pady=(60, 4))

        tk.Label(self, text=f"Logged in as: {role}",
                 bg=self.current_bg, fg=self.current_text,
                 font=FONT_NORMAL).pack(pady=(0, 30))

        # Logout button
        tk.Button(self, text="Logout",
                  bg=SEC_BTN_BG, fg=BTN_FG,
                  activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_HEADER, width=24, cursor="hand2",
                  command=self._logout).pack(pady=10, ipady=6)

        if role == "admin":
            tk.Button(self, text="View All Students",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self._view_all_students).pack(pady=10, ipady=6)

            tk.Button(self, text="Add Student",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self._add_student).pack(pady=10, ipady=6)
        else:
            tk.Button(self, text="View My Record",
                      bg=ACCENT, fg=BTN_FG, activebackground=MAIN_BTN_BG_CLICK,
                      activeforeground=BTN_FG, relief="raised",
                      font=FONT_HEADER, width=24, cursor="hand2",
                      command=self._view_my_record).pack(pady=10, ipady=6)

    # TODO
    def _view_all_students(self):
        pass

    # TODO
    def _add_student(self):
        pass

    # TODO
    def _view_my_record(self):
        pass

    def _logout(self):
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
        self._build()
        self.app._apply_colors(self, bg, card, text, entry)
        title_fg = DARK_TEXT if self.app.dark_mode else ACCENT
        self.title_label.configure(fg=title_fg)

if __name__ == "__main__":
    app = SecureStudentApp()
    app.run()