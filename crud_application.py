import psycopg2
from psycopg2 import sql
from datetime import date


def connect_to_database():
    dbname = 'assignment3'
    user = 'postgres'
    password = 'TitanFries15'
    host = 'localhost'
    port = 5433

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    return conn


def close_connection(conn):
    conn.close()


def getAllStudents():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return students


def addStudent(first_name, last_name, email, enrollment_date):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (first_name, last_name, email, enrollment_date) 
        VALUES (%s, %s, %s, %s)""", (first_name, last_name, email, enrollment_date))
    conn.commit()
    cursor.close()
    close_connection(conn)


def updateStudentEmail(student_id, new_email):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students 
        SET email = %s 
        WHERE student_id = %s""", (new_email, student_id))
    conn.commit()
    cursor.close()
    close_connection(conn)


def deleteStudent(student_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM students 
        WHERE student_id = %s""", (student_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)


# Infinite loop for user interaction
while True:
    print("\nOptions:")
    print("1. Get all students")
    print("2. Add a student")
    print("3. Update student email")
    print("4. Delete a student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        students = getAllStudents()
        print("All Students:")
        for student in students:
            print(student)
    elif choice == '2':
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
        addStudent(first_name, last_name, email, enrollment_date)
        print("Student added successfully.")
    elif choice == '3':
        student_id = input("Enter student ID: ")
        new_email = input("Enter new email: ")
        updateStudentEmail(student_id, new_email)
        print("Email updated successfully.")
    elif choice == '4':
        student_id = input("Enter student ID: ")
        deleteStudent(student_id)
        print("Student deleted successfully.")
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
