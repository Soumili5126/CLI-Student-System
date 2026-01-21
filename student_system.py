import psycopg2
import json
import os


# DATABASE CONNECTION
def get_db_connection():
    return psycopg2.connect(
        dbname="student_crud_db",
        user="st_user",
        password="password1234",
        host="localhost",
        port=5432
    )

# JSON HELPERS
def load_json(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r") as file:
        return json.load(file)

def save_json(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)



# INSTRUCTOR CRUD
def add_instructor():
    conn = get_db_connection()
    cur = conn.cursor()

    fname = input("First Name: ")
    lname = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    dep_id = int(input("Department ID: "))

    cur.execute("""
        INSERT INTO instructor (fname, lname, email, phone, dep_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING ins_id
    """, (fname, lname, email, phone, dep_id))

    ins_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("instructors.json")
    data.append({
        "ins_id": ins_id,
        "fname": fname,
        "lname": lname,
        "email": email,
        "phone": phone,
        "dep_id": dep_id
    })
    save_json("instructors.json", data)

    print("Instructor added")


def view_instructors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM instructor")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()


def update_instructor():
    ins_id = int(input("Instructor ID to update: "))
    email = input("New Email: ")
    phone = input("New Phone: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE instructor
        SET email=%s, phone=%s
        WHERE ins_id=%s
    """, (email, phone, ins_id))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("instructors.json")
    for i in data:
        if i["ins_id"] == ins_id:
            i["email"] = email
            i["phone"] = phone
    save_json("instructors.json", data)

    print("Instructor updated")


def delete_instructor():
    ins_id = int(input("Instructor ID to delete: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM instructor WHERE ins_id=%s", (ins_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("instructors.json")
    data = [i for i in data if i["ins_id"] != ins_id]
    save_json("instructors.json", data)

    print("Instructor deleted")

# DEPARTMENT CRUD
def add_department():
    conn = get_db_connection()
    cur = conn.cursor()

    name = input("Department Name: ")
    hod = input("HOD Name: ")

    cur.execute("""
        INSERT INTO department (name, hod, nstudent, ninstructor)
        VALUES (%s, %s, %s, %s)
        RETURNING dep_id
    """, (name, hod))

    dep_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("departments.json")
    data.append({"dep_id": dep_id, "name": name, "hod": hod})
    save_json("departments.json", data)

    print("Department added")

def view_departments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM department")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def update_department():
    dep_id = int(input("Department ID to update: "))
    name = input("New Name: ")
    hod = input("New HOD: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE department SET name=%s, hod=%s WHERE dep_id=%s
    """, (name, hod, dep_id))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("departments.json")
    for d in data:
        if d["dep_id"] == dep_id:
            d["name"] = name
            d["hod"] = hod
    save_json("departments.json", data)

    print("Department updated")

def delete_department():
    dep_id = int(input("Department ID to delete: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM department WHERE dep_id=%s", (dep_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("departments.json")
    data = [d for d in data if d["dep_id"] != dep_id]
    save_json("departments.json", data)

    print("Department deleted")


# STUDENT CRUD
def add_student():
    conn = get_db_connection()
    cur = conn.cursor()

    fname = input("First Name: ")
    lname = input("Last Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    gender = input("Gender: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    dep_id = int(input("Department ID: "))

    cur.execute("""
        INSERT INTO student (fname,lname,dob,gender,email,phone,address,dep_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING stud_id
    """, (fname, lname, dob, gender, email, phone, address, dep_id))

    stud_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("students.json")
    data.append({
        "stud_id": stud_id,
        "fname": fname,
        "lname": lname,
        "dob": dob,
        "gender": gender,
        "email": email,
        "phone": phone,
        "address": address,
        "dep_id": dep_id
    })
    save_json("students.json", data)

    print("Student added")

def view_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def update_student():
    stud_id = int(input("Student ID to update: "))
    email = input("New Email: ")
    phone = input("New Phone: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE student SET email=%s, phone=%s WHERE stud_id=%s
    """, (email, phone, stud_id))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("students.json")
    for s in data:
        if s["stud_id"] == stud_id:
            s["email"] = email
            s["phone"] = phone
    save_json("students.json", data)

    print("Student updated")

def delete_student():
    stud_id = int(input("Student ID to delete: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE stud_id=%s", (stud_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("students.json")
    data = [s for s in data if s["stud_id"] != stud_id]
    save_json("students.json", data)

    print("Student deleted")


# COURSE CRUD
def add_course():
    conn = get_db_connection()
    cur = conn.cursor()

    name = input("Course Name: ")
    code = input("Course Code: ")
    credits = int(input("Credits: "))
    dep_id = int(input("Department ID: "))

    cur.execute("""
        INSERT INTO course (name,code,credits,dep_id)
        VALUES (%s,%s,%s,%s)
        RETURNING course_id
    """, (name, code, credits, dep_id))

    course_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("courses.json")
    data.append({
        "course_id": course_id,
        "name": name,
        "code": code,
        "credits": credits,
        "dep_id": dep_id
    })
    save_json("courses.json", data)

    print("Course added")

def view_courses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM course")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def update_course():
    course_id = int(input("Course ID to update: "))
    credits = int(input("New Credits: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE course SET credits=%s WHERE course_id=%s
    """, (credits, course_id))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("courses.json")
    for c in data:
        if c["course_id"] == course_id:
            c["credits"] = credits
    save_json("courses.json", data)

    print("Course updated")

def delete_course():
    course_id = int(input("Course ID to delete: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM course WHERE course_id=%s", (course_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("courses.json")
    data = [c for c in data if c["course_id"] != course_id]
    save_json("courses.json", data)

    print("Course deleted")


# ENROLLMENT CRUD
def enroll_student():
    conn = get_db_connection()
    cur = conn.cursor()

    stud_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))
    grade = input("Grade: ")
    date = input("Date (YYYY-MM-DD): ")

    cur.execute("""
        INSERT INTO enrollment (stud_id,course_id,grade,date)
        VALUES (%s,%s,%s,%s)
        RETURNING en_id
    """, (stud_id, course_id, grade, date))

    en_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("enrollments.json")
    data.append({
        "en_id": en_id,
        "stud_id": stud_id,
        "course_id": course_id,
        "grade": grade,
        "date": date
    })
    save_json("enrollments.json", data)

    print("Enrollment added")

def view_enrollments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM enrollment")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def update_enrollment():
    en_id = int(input("Enrollment ID to update: "))
    grade = input("New Grade: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE enrollment SET grade=%s WHERE en_id=%s
    """, (grade, en_id))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("enrollments.json")
    for e in data:
        if e["en_id"] == en_id:
            e["grade"] = grade
    save_json("enrollments.json", data)

    print("Enrollment updated")

def delete_enrollment():
    en_id = int(input("Enrollment ID to delete: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM enrollment WHERE en_id=%s", (en_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("enrollments.json")
    data = [e for e in data if e["en_id"] != en_id]
    save_json("enrollments.json", data)

    print("Enrollment deleted")

# MAIN MENU
def menu():
    while True:
        print("\n--- STUDENT MANAGEMENT SYSTEM ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Add Course")
        print("6. View Courses")
        print("7. Update Course")
        print("8. Delete Course")
        print("9. Enroll Student")
        print("10. View Enrollments")
        print("11. Update Enrollment")
        print("12. Delete Enrollment")
        print("13. Add Department")
        print("14. View Department")
        print("15. Update Department")
        print("16. Delete Department")
        print("17. Add Instructor")
        print("18. View Instructor")
        print("19. Update Instructor")
        print("20. Delete Instructor")
        print("21. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            add_course()
        elif choice == "6":
            view_courses()
        elif choice == "7":
            update_course()
        elif choice == "8":
            delete_course()
        elif choice == "9":
            enroll_student()
        elif choice == "10":
            view_enrollments()
        elif choice == "11":
            update_enrollment()
        elif choice == "12":
            delete_enrollment()
        elif choice == "13":
            add_department()
        elif choice == "14":
            view_departments()
        elif choice == "15":
            update_department()
        elif choice == "16":
            delete_department()
        elif choice == "17":
            add_instructor()
        elif choice == "18":
            view_instructors()
        elif choice == "19":
            update_instructor()
        elif choice == "20":
            delete_instructor()
        elif choice == "21":
            print("Exiting system...")
            break
        else:
            print("Invalid choice")


# START PROGRAM

menu()




