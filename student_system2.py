import psycopg2
import json
import os


# DATABASE CONNECTION
def get_db_connection():
    return psycopg2.connect(
        dbname="student_database",
        user="e_users",
        password="password1234",
        host="localhost",
        port=5432
    )


# JSON HELPERS
def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# DEPARTMENT CRUD
def add_department():
    conn = get_db_connection()
    cur = conn.cursor()

    name = input("Department Name: ")
    hod = input("HOD Name: ")

    cur.execute("""
        INSERT INTO department (name, hod)
        VALUES (%s, %s)
        RETURNING dep_id
    """, (name, hod))

    dep_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("departments.json")
    data.append({
        "dep_id": dep_id,
        "name": name,
        "hod": hod
    })
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
    dep_id = int(input("Department ID: "))
    name = input("New Department Name: ")
    hod = input("New HOD Name: ")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE department
        SET name=%s, hod=%s
        WHERE dep_id=%s
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
    dep_id = int(input("Department ID: "))

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


# ROLE CRUD
def add_role():
    conn = get_db_connection()
    cur = conn.cursor()

    role_name = input("Role Name (STUDENT / INSTRUCTOR): ").upper()

    cur.execute("""
        INSERT INTO role (role_name)
        VALUES (%s)
        RETURNING role_id
    """, (role_name,))

    role_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("roles.json")
    data.append({
        "role_id": role_id,
        "role_name": role_name
    })
    save_json("roles.json", data)

    print("Role added successfully")


def view_roles():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT role_id, role_name FROM role")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def update_role():
    role_id = int(input("Role ID to update: "))
    new_role_name = input("New Role Name (STUDENT / INSTRUCTOR): ").upper()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE role
        SET role_name = %s
        WHERE role_id = %s
    """, (new_role_name, role_id))

    conn.commit()
    cur.close()
    conn.close()

    data = load_json("roles.json")
    for r in data:
        if r["role_id"] == role_id:
            r["role_name"] = new_role_name
    save_json("roles.json", data)

    print("Role updated successfully")


def delete_role():
    role_id = int(input("Role ID to delete: "))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM role WHERE role_id = %s", (role_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("roles.json")
    data = [r for r in data if r["role_id"] != role_id]
    save_json("roles.json", data)

    print("Role deleted successfully")



# USER CRUD
def add_user():
    conn = get_db_connection()
    cur = conn.cursor()

    fname = input("First Name: ")
    lname = input("Last Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    gender = input("Gender: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    role_id = int(input("Role ID: "))

    cur.execute("""
        INSERT INTO users
        (fname,lname,dob,gender,email,phone,address,role_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING user_id
    """, (fname, lname, dob, gender, email, phone, address, role_id))

    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("users.json")
    data.append({
        "user_id": user_id,
        "fname": fname,
        "lname": lname,
        "dob": dob,
        "gender": gender,
        "email": email,
        "phone": phone,
        "address": address,
        "role_id": role_id
    })
    save_json("users.json", data)

    print("User added")

def view_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.fname, u.lname, r.role_name
        FROM users u
        JOIN role r ON u.role_id = r.role_id
    """)
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def update_user():
    user_id = int(input("User ID: "))
    email = input("New Email: ")
    phone = input("New Phone: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET email=%s, phone=%s WHERE user_id=%s
    """, (email, phone, user_id))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("users.json")
    for u in data:
        if u["user_id"] == user_id:
            u["email"] = email
            u["phone"] = phone
    save_json("users.json", data)

    print("User updated")

def delete_user():
    user_id = int(input("User ID: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("users.json")
    data = [u for u in data if u["user_id"] != user_id]
    save_json("users.json", data)

    print("User deleted")


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


# ENROLLMENT CRUD
def enroll_student():
    conn = get_db_connection()
    cur = conn.cursor()

    user_id = int(input("Student User ID: "))
    course_id = int(input("Course ID: "))
    grade = input("Grade: ")
    date = input("Date (YYYY-MM-DD): ")

    cur.execute("""
        SELECT r.role_name
        FROM users u
        JOIN role r ON u.role_id = r.role_id
        WHERE u.user_id=%s
    """, (user_id,))
    role = cur.fetchone()

    if not role or role[0] != "STUDENT":
        print("Only STUDENT role can enroll")
        conn.close()
        return

    cur.execute("""
        INSERT INTO enrollment (user_id,course_id,grade,date)
        VALUES (%s,%s,%s,%s)
        RETURNING en_id
    """, (user_id, course_id, grade, date))

    en_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    data = load_json("enrollments.json")
    data.append({
        "en_id": en_id,
        "user_id": user_id,
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


# MAIN MENU
def menu():
    while True:
        print("\n--- STUDENT MANAGEMENT SYSTEM ---")
        print("1. Add Role")
        print("2. View Roles")
        print("3. Add User")
        print("4. View Users")
        print("5. Update User")
        print("6. Delete User")
        print("7. Add Course")
        print("8. View Courses")
        print("9. Enroll Student")
        print("10. View Enrollments")
        print("11. Exit")

        ch = input("Choose option: ")

        if ch == "1":
            add_role()
        elif ch == "2":
            view_roles()
        elif ch == "3":
            add_user()
        elif ch == "4":
            view_users()
        elif ch == "5":
            update_user()
        elif ch == "6":
            delete_user()
        elif ch == "7":
            add_course()
        elif ch == "8":
            view_courses()
        elif ch == "9":
            enroll_student()
        elif ch == "10":
            view_enrollments()
        elif ch == "11":
            break
        else:
            print("Invalid choice")


# START

menu()
