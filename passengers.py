"""passengers.py — Passenger registration and profile management (CRUD)."""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="root", database="flight_2026")


def add_passenger():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Passenger ID: "))
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender (M/F/O): ")
    phone = input("Phone: ")
    email = input("Email: ")
    passport = input("Passport No: ")
    cur.execute("INSERT INTO passengers VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (pid, name, age, gender, phone, email, passport))
    con.commit()
    print("Passenger added successfully.")
    con.close()


def view_passengers():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM passengers")
    rows = cur.fetchall()
    print(f"{'ID':<5}{'Name':<25}{'Age':<5}{'Gender':<8}{'Phone':<15}{'Passport'}")
    print("-" * 75)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<25}{r[2]:<5}{r[3]:<8}{r[4]:<15}{r[6]}")
    con.close()


def search_passenger():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Passenger ID: "))
    cur.execute("SELECT * FROM passengers WHERE passenger_id=%s", (pid,))
    r = cur.fetchone()
    if r:
        print(f"ID: {r[0]}\nName: {r[1]}\nAge: {r[2]}\nGender: {r[3]}\n"
              f"Phone: {r[4]}\nEmail: {r[5]}\nPassport: {r[6]}")
    else:
        print("Passenger not found.")
    con.close()


def update_passenger():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Passenger ID: "))
    phone = input("New Phone: ")
    email = input("New Email: ")
    cur.execute("UPDATE passengers SET phone=%s, email=%s WHERE passenger_id=%s",
                (phone, email, pid))
    con.commit()
    print("Passenger updated." if cur.rowcount else "Passenger not found.")
    con.close()


def delete_passenger():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Passenger ID: "))
    cur.execute("DELETE FROM passengers WHERE passenger_id=%s", (pid,))
    con.commit()
    print("Passenger deleted." if cur.rowcount else "Passenger not found.")
    con.close()


def menu():
    while True:
        print("\n--- PASSENGERS ---")
        print("1. Add Passenger")
        print("2. View All Passengers")
        print("3. Search Passenger")
        print("4. Update Contact Info")
        print("5. Delete Passenger")
        print("6. Back")
        ch = input("Choice: ")
        if ch == "1": add_passenger()
        elif ch == "2": view_passengers()
        elif ch == "3": search_passenger()
        elif ch == "4": update_passenger()
        elif ch == "5": delete_passenger()
        elif ch == "6": break
        else: print("Invalid choice.")
