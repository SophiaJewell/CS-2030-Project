"""
database_handler.py

Purpose:
This module handles all reading and writing for database.json.

File purpose:
- Creates the database if it does not exist
- Loads data from JSON
- Saves data to JSON
- Gets users and students
- Finds specific users and students
- Adds users and students
- Updates or deletes students
- Updates users if needed later

Why this matters:
The project requires persistent storage using JSON and proper exception handling.
This file keeps all database-related logic in one place.
"""

import json
import os


DATABASE_FILE = "database.json"


def initialize_database():
    """
    Create database.json with the required structure if it does not exist.

    Required top-level keys:
    - users
    - students

    This prevents file-not-found errors when the program runs for the first time.
    """
    if not os.path.exists(DATABASE_FILE):
        default_data = {
            "users": [],
            "students": []
        }
        save_database(default_data)


def load_database():
    """
    Load and return the full database.

    Returns:
        dict: The full database dictionary.

    Raises:
        ValueError: If the file exists but contains invalid JSON or invalid structure.
        OSError: If there is a file access problem.
    """
    initialize_database()

    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Database structure is invalid. Root must be a dictionary.")

        if "users" not in data or "students" not in data:
            raise ValueError("Database structure is invalid. Missing 'users' or 'students' key.")

        if not isinstance(data["users"], list) or not isinstance(data["students"], list):
            raise ValueError("'users' and 'students' must both be lists.")

        return data

    except json.JSONDecodeError as error:
        raise ValueError(f"Database file is corrupted or not valid JSON: {error}")
    except OSError as error:
        raise OSError(f"Error reading database file: {error}")


def save_database(data):
    """
    Save the full database dictionary to database.json.

    Parameters:
        data (dict): The full database structure to save.

    Raises:
        TypeError --> data is not a dictionary.
        OSError --> there is a file write problem.
    """
    if not isinstance(data, dict):
        raise TypeError("Database data must be a dictionary.")

    try:
        with open(DATABASE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        raise OSError(f"Error saving database file: {error}")


def get_users():
    """
    Return the list of all users.

    Returns:
        list: List of user dictionaries.
    """
    return load_database()["users"]


def get_students():
    """
    Return the list of all students.

    Returns:
        list: List of student dictionaries.
    """
    return load_database()["students"]


def find_user_by_email(email):
    """
    Find a user by email address.

    Parameters:
        email (str): The email to search for.

    Returns:
        dict or None: The matching user if found, otherwise None.
    """
    for user in get_users():
        if user.get("email", "").lower() == email.lower():
            return user
    return None


def find_student_by_id(student_id):
    """
    Find a student by student ID / 700 number.

    Parameters:
        student_id (str): The student ID to search for.

    Returns:
        dict or None: The matching student if found, otherwise None.
    """
    for student in get_students():
        if student.get("student_id") == student_id:
            return student
    return None


def add_user(user_data):
    """
    Add a new user to the database.

    Expected fields:
    - email
    - password
    - role

    Parameters:
        user_data (dict): The new user record.

    Raises:
        TypeError: If user_data is not a dictionary.
        ValueError: If required fields are missing or email already exists.
    """
    if not isinstance(user_data, dict):
        raise TypeError("User data must be a dictionary.")

    required_fields = {"email", "password", "role"}
    missing_fields = required_fields - user_data.keys()

    if missing_fields:
        raise ValueError(f"Missing required user field(s): {', '.join(sorted(missing_fields))}")

    if find_user_by_email(user_data["email"]) is not None:
        raise ValueError("A user with that email already exists.")

    data = load_database()
    data["users"].append(user_data)
    save_database(data)


def add_student(student_data):
    """
    Add a new student to the database.

    Expected fields:
    - student_id
    - first_name
    - last_name
    - age
    - gender
    - phone

    Parameters:
        student_data (dict): The new student record.

    Raises:
        TypeError: If student_data is not a dictionary.
        ValueError: If required fields are missing or student ID already exists.
    """
    if not isinstance(student_data, dict):
        raise TypeError("Student data must be a dictionary.")

    required_fields = {"student_id", "first_name", "last_name", "age", "gender", "phone"}
    missing_fields = required_fields - student_data.keys()

    if missing_fields:
        raise ValueError(f"Missing required student field(s): {', '.join(sorted(missing_fields))}")

    if find_student_by_id(student_data["student_id"]) is not None:
        raise ValueError("A student with that 700 number already exists.")

    data = load_database()
    data["students"].append(student_data)
    save_database(data)


def update_user(email, updated_fields):
    """
    Update an existing user record.

    Parameters:
        email (str): The email of the user to update.
        updated_fields (dict): A dictionary of fields to change.

    Raises:
        TypeError: If updated_fields is not a dictionary.
        ValueError: If the user is not found.
    """
    if not isinstance(updated_fields, dict):
        raise TypeError("Updated fields must be provided as a dictionary.")

    data = load_database()

    for user in data["users"]:
        if user.get("email", "").lower() == email.lower():
            user.update(updated_fields)
            save_database(data)
            return

    raise ValueError("User not found.")


def update_student(student_id, updated_fields):
    """
    Update an existing student record.

    Parameters:
        student_id (str): The ID of the student to update.
        updated_fields (dict): A dictionary of fields to change.

    Raises:
        TypeError: If updated_fields is not a dictionary.
        ValueError: If the student is not found.
    """
    if not isinstance(updated_fields, dict):
        raise TypeError("Updated fields must be provided as a dictionary.")

    data = load_database()

    for student in data["students"]:
        if student.get("student_id") == student_id:
            student.update(updated_fields)
            save_database(data)
            return

    raise ValueError("Student not found.")


def delete_student(student_id):
    """
    Delete a student from the database by student ID.

    Parameters:
        student_id (str): The ID of the student to remove.

    Raises:
        ValueError: If the student does not exist.
    """
    data = load_database()

    for index, student in enumerate(data["students"]):
        if student.get("student_id") == student_id:
            del data["students"][index]
            save_database(data)
            return

    raise ValueError("Student not found.")


def delete_user(email):
    """
    Delete a user from the database by email.

    Parameters:
        email (str): The email of the user to remove.

    Raises:
        ValueError: If the user does not exist.
    """
    data = load_database()

    for index, user in enumerate(data["users"]):
        if user.get("email", "").lower() == email.lower():
            del data["users"][index]
            save_database(data)
            return

    raise ValueError("User not found.")

def get_grades(student_id):
    """
    Return the grades list for a specific student.

    Parameters:
        student_id (str): The student ID to search for.

    Returns:
        list: The grades list, or an empty list if none found.
    """
    data = load_database()
    for student in data["students"]:
        if student.get("student_id") == student_id:
            return student.get("grades", [])
    return []


def save_grades(student_id, grades):
    """
    Save a grades list to a specific student's record.

    Parameters:
        student_id (str): The student ID to update.
        grades (list): The grades list to save.

    Raises:
        ValueError: If the student is not found.
    """
    data = load_database()
    for student in data["students"]:
        if student.get("student_id") == student_id:
            student["grades"] = grades
            save_database(data)
            return
    raise ValueError("Student not found.")