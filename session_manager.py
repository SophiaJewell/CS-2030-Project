"""
session_manager.py

Manages the active user's session state.
tracks login attempts.
"""

MAX_ATTEMPTS = 4 # Limit to User's incorrect logins

class SessionManager:

    def __init__(self):
        self._current_email   = None
        self._current_role    = None
        self._failed_attempts = 0

    def is_logged_in(self):
        # Returns true if users logins successfully
        return self._current_email is not None

    def is_locked_out(self):
        # Returns True if failed attempts reaches limit
        return self._failed_attempts >= MAX_ATTEMPTS

    def attempts_remaining(self):
        # Returns how many tries are left
        return max(0, MAX_ATTEMPTS - self._failed_attempts)

    def get_current_email(self):
        # Get user's email
        return self._current_email

    def get_current_role(self):
        # Get user's role
        return self._current_role

    def login(self, email, role="user"):
        # Update user's info with successful login
        self._current_email = email
        self._current_role = role
        self._failed_attempts = 0

    def logout(self):
        # Log user out, set variables to original values
        self._current_email = None
        self._current_role = None
        self._failed_attempts = 0

    def record_failed_attempt(self):
        # Increase fail counter +1 when login fails
        self._failed_attempts += 1

    def reset_attempts(self):
        # Reset failed attempt counter
        self._failed_attempts = 0