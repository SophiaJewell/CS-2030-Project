"""
security.py

Purpose:
This module handles password security for the Secure Student Management System.

What this file does:
- Hashes passwords using SHA-256
- Verifies whether an entered password matches a stored hash

Why this matters:
The project instructions require that passwords are never stored in plaintext.
Instead of saving the actual password, we save a SHA-256 hash of it.
"""

import hashlib


def hash_password(password):
    """
    Convert a plain-text password into a SHA-256 hash.

    Parameters:
        password (str): The user's original password.

    Returns:
        str: The SHA-256 hash as a hexadecimal string.

    Example:
        >>> hash_password("!Abc123")
        '...some long hash string...'
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    # hashlib requires bytes, so we encode the string first.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password, stored_hash):
    """
    Check whether a plain-text password matches a stored hash.

    Parameters:
        plain_password (str): The password the user entered during login.
        stored_hash (str): The saved SHA-256 hash from the database.

    Returns:
        bool: True if the password is correct, False otherwise.

    How it works:
    - Hash the entered password
    - Compare the new hash to the stored hash
    """
    if not isinstance(plain_password, str):
        raise TypeError("Password must be a string.")

    if not isinstance(stored_hash, str):
        raise TypeError("Stored hash must be a string.")

    return hash_password(plain_password) == stored_hash