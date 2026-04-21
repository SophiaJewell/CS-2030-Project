"""
main.py

Controller layer - Main application entry point

Manages the Tkinter GUI window
handles navigation between screens
"""
import tkinter as tk
from tkinter import messagebox

from session_manager import SessionManager

# Colors
BG_COLOR   = "#dbeafe"
CARD_COLOR = "#cbdaee"

ACCENT     = "#1e3a8a"
TEXT_COLOR = "#111111"

ENTRY_BG   = "#fbfafe"

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
        self.root.resizable(True, True)
        self.root.configure(bg=BG_COLOR)

        # Create the session manager
        self.session = SessionManager()

        # Container that holds all screens stacked on top of each other
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Store all screens in a dictionary
        self.frames = {}
        for ScreenClass in (WelcomeFrame, LoginFrame, RegisterFrame):
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
        tk.Label(self, text="Student Management System",
                 bg=BG_COLOR, fg=ACCENT,
                 font=FONT_TITLE).pack(pady=(140, 60))

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
            self.app.set_status("Please fill in all fields.", ok=False)
            return

        # Check if already locked out
        if self.app.session.is_locked_out():
            messagebox.showerror("Locked Out", "Too many failed attempts.")
            self._go_back()
            return

        # TODO: Replace with function that authenticates user
        # Temp created login
        success = (email == "admin@gmail.com" and password == "Admin1")

        if success:
            self.app.session.login(email)
            self.app.set_status(f"Welcome, {email}!", ok=True)
            messagebox.showinfo("Success", f"Logged in as {email}")
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

        # Register button
        tk.Button(btn_row, text="Back",
                  bg=SEC_BTN_BG , fg=BTN_FG, activebackground=SEC_BTN_BG_CLICK,
                  activeforeground=BTN_FG, relief="raised",
                  font=FONT_NORMAL, width=8, cursor="hand2",
                  command=self._go_back).pack(side="left", padx=8, ipady=10)

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
            self.app.set_status("All fields are required.", ok=False)
            return

        # Check if passwords match
        if pw != confirm:
            messagebox.showwarning("Mismatch", "Passwords do not match.")
            self.app.set_status("Passwords do not match.", ok=False)
            return

        # TODO: Replace with email/password validation, and save info after password hash.
        self.app.set_status(f"Account created for {email}!", ok=True)
        messagebox.showinfo("Registered", f"Account created!\nEmail: {email}")
        self.app.show_frame(WelcomeFrame)

    def _go_back(self):
        self.app.show_frame(WelcomeFrame)

if __name__ == "__main__":
    app = SecureStudentApp()
    app.run()