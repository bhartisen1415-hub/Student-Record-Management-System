import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent
CSV_FILE = DATA_DIR / "students.csv"
JSON_FILE = DATA_DIR / "students.json"
FIELDS = ["student_id", "name", "age", "course", "email"]


def load_students():
    """Load student records from JSON, falling back to CSV or an empty list."""
    try:
        if JSON_FILE.exists():
            with JSON_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        if CSV_FILE.exists():
            with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
                return list(csv.DictReader(file))
    except (OSError, json.JSONDecodeError, csv.Error) as error:
        print(f"Warning: Could not read saved records: {error}")
    return []


def save_students(students):
    """Save records to both JSON and CSV formats."""
    try:
        with JSON_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)

        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)
    except OSError as error:
        print(f"Error: Could not save records: {error}")


def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def add_student(students):
    student_id = get_nonempty("Student ID: ")
    if any(s["student_id"] == student_id for s in students):
        print("A student with this ID already exists.")
        return

    name = get_nonempty("Full name: ")
    while True:
        try:
            age = int(input("Age: ").strip())
            if 1 <= age <= 120:
                break
            print("Age must be between 1 and 120.")
        except ValueError:
            print("Please enter age as a whole number.")

    course = get_nonempty("Course: ")
    email = get_nonempty("Email: ")
    student = {
        "student_id": student_id,
        "name": name,
        "age": str(age),
        "course": course,
        "email": email,
    }
    students.append(student)
    save_students(students)
    print("Student added successfully.")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n" + "-" * 88)
    print(f"{'ID':<12} {'NAME':<22} {'AGE':<6} {'COURSE':<20} {'EMAIL':<25}")
    print("-" * 88)
    for student in students:
        print(
            f"{student.get('student_id', '')[:11]:<12} "
            f"{student.get('name', '')[:21]:<22} "
            f"{student.get('age', ''):<6} "
            f"{student.get('course', '')[:19]:<20} "
            f"{student.get('email', '')[:24]:<25}"
        )
    print("-" * 88)


def find_student(students, student_id):
    return next((s for s in students if s.get("student_id") == student_id), None)


def update_student(students):
    student_id = get_nonempty("Enter the ID of the student to update: ")
    student = find_student(students, student_id)
    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep the current value.")
    for field in ["name", "age", "course", "email"]:
        current = student.get(field, "")
        new_value = input(f"{field.title()} [{current}]: ").strip()
        if not new_value:
            continue
        if field == "age":
            try:
                age = int(new_value)
                if not 1 <= age <= 120:
                    print("Invalid age; keeping the old value.")
                    continue
                new_value = str(age)
            except ValueError:
                print("Invalid age; keeping the old value.")
                continue
        student[field] = new_value

    save_students(students)
    print("Student record updated successfully.")


def delete_student(students):
    student_id = get_nonempty("Enter the ID of the student to delete: ")
    student = find_student(students, student_id)
    if not student:
        print("Student not found.")
        return

    confirm = input(f"Delete {student.get('name')} (ID {student_id})? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student record deleted.")
    else:
        print("Delete cancelled.")


def search_student(students):
    query = get_nonempty("Search by student ID or name: ").lower()
    matches = [
        s for s in students
        if query in s.get("student_id", "").lower()
        or query in s.get("name", "").lower()
    ]
    view_students(matches)


def main():
    students = load_students()
    actions = {
        "1": add_student,
        "2": view_students,
        "3": update_student,
        "4": delete_student,
        "5": search_student,
    }

    while True:
        print("\n=== STUDENT RECORD MANAGEMENT SYSTEM ===")
        print("1. Add student")
        print("2. View all students")
        print("3. Update student")
        print("4. Delete student")
        print("5. Search student")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()

        if choice == "6":
            print("Thank you for using the Student Record Management System!")
            break
        action = actions.get(choice)
        if action:
            try:
                action(students)
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled.")
            except Exception as error:
                print(f"An unexpected error occurred: {error}")
        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()
