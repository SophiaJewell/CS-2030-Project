"""
validator.py

Purpose:
This module validates user and student input for the Secure Student Management System.

Types of data to validate:
- Names
- Phone numbers
- Email addresses
- Passwords

Design choice:
Each validation function returns a tuple:
    (True, "Success message")
or
    (False, "error message")

This simplifies communication with the controller layer to display feedback to the user.
"""

import re


def validate_name(name):
    """
    Validate a first or last name.

    Rules:
    - Must start with a capital letter
    - Must contain only letters
    - Must be at least 2 letters long
    - No digits or special characters allowed

    Parameters:
        name (str): The name to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(name, str):
        return False, "Name must be a string."

    name = name.strip()

    if not name:
        return False, "Name cannot be empty."

    # Pattern explanation:
    # ^        start of string
    # [A-Z]    first character must be uppercase
    # [a-z]+   one or more lowercase letters after it
    # $        end of string
    pattern = r"^[A-Z][a-z]+$"

    if re.fullmatch(pattern, name):
        return True, "Valid name."

    return False, (
        "Invalid name. Name must start with a capital letter, contain only letters, "
        "and be at least 2 letters long."
    )


def validate_phone(phone):
    """
    Validate a phone number.

    Required format:
    123-456-7890

    Parameters:
        phone (str): The phone number to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(phone, str):
        return False, "Phone number must be a string."

    phone = phone.strip()

    if not phone:
        return False, "Phone number cannot be empty."

    pattern = r"^\d{3}-\d{3}-\d{4}$"

    if re.fullmatch(pattern, phone):
        return True, "Valid phone number."

    return False, "Invalid phone number. Use the format xxx-xxx-xxxx."


def validate_email(email):
    """
    Validate an email address.

    Project rule:
    Only Gmail, Yahoo, or UCMO email addresses should be accepted.

    Accepted examples:
    - user@gmail.com
    - user@yahoo.com
    - user@ucmo.edu

    Parameters:
        email (str): The email address to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(email, str):
        return False, "Email must be a string."

    email = email.strip()

    if not email:
        return False, "Email cannot be empty."

    # Allows a normal username before @
    # Then only gmail, yahoo, or ucmo
    # Then a normal top-level domain such as .com or .edu
    pattern = r"^[A-Za-z0-9._%+-]+@(gmail|yahoo|ucmo)\.[A-Za-z]{2,}$"

    if re.fullmatch(pattern, email):
        return True, "Valid email."

    return False, (
        "Invalid email. Only Gmail, Yahoo, or UCMO email addresses are allowed "
        "(example: user@gmail.com)."
    )


def validate_password(password):
    """
    Validate a password according to the project rules.

    Required rules:
    - Must start with one of ! @ # $ % ^ & *
    - Must be 6 to 12 characters long
    - Must contain at least 1 digit
    - Must contain at least 1 uppercase letter
    - Must contain at least 1 lowercase letter

    Parameters:
        password (str): The password to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(password, str):
        return False, "Password must be a string."

    if not password:
        return False, "Password cannot be empty."

    allowed_start_characters = "!@#$%^&*"

    if len(password) < 6 or len(password) > 12:
        return False, "Invalid password. It must be between 6 and 12 characters long."

    if password[0] not in allowed_start_characters:
        return False, "Invalid password. It must start with one of these: !@#$%^&*"

    if not re.search(r"[A-Z]", password):
        return False, "Invalid password. It must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Invalid password. It must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Invalid password. It must contain at least one digit."

    return True, "Valid password."


def validate_age(age):
    """
    Validate a student's age.

    Project rule:
    Age must be between 16 and 100.

    Parameters:
        age (int or str): The age value to validate.

    Returns:
        tuple: (bool, str)
    """
    try:
        age = int(age)
    except (TypeError, ValueError):
        return False, "Invalid age. Age must be a whole number."

    if 16 <= age <= 100:
        return True, "Valid age."

    return False, "Invalid age. Age must be between 16 and 100."


def validate_student_id(student_id):
    """
    Validate a student 700 number.

    Student ID rule:
    A 700 is 9 digits and always begins with 700.

    Examples:
    - 700123456 -> valid
    - 701123456 -> invalid

    Parameters:
        student_id (str): The student ID to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(student_id, str):
        return False, "Student ID must be a string."

    student_id = student_id.strip()

    if not student_id:
        return False, "Student ID cannot be empty."

    pattern = r"^700\d{6}$"

    if re.fullmatch(pattern, student_id):
        return True, "Valid student ID."

    return False, "Invalid student ID. Must be a 9-digit number that starts with 700."

