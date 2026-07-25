"""flights.py — Flight schedule management: add, view, search by route, update fare, delete."""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="root", database="flight_2026")


def add_flight():
    con = _connect()
    cur = con.cursor()
    fid = int(input("Flight ID: "))
    fno = input("Flight No (e.g. AI-101): ")
    airline = input("Airline: ")
    src = input("Source city: ")
    dst = input("Destination city: ")
    dep = input("Departure time (HH:MM): ")
    arr = input("Arrival time (HH:MM): ")
    date = input("Travel Date (YYYY-MM-DD): ")
    seats = int(input("Total Seats: "))
    fare = int(input("Fare (Rs.): "))
    cur.execute("INSERT INTO flights VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (fid, fno, airline, src, dst, dep, arr, date, seats, seats, fare))
    con.commit()
    print("Flight added successfully.")
    con.close()


def view_flights():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT flight_id, flight_no, airline, source, destination, dep_time, arr_time, travel_date, seats_left, fare FROM flights")
    rows = cur.fetchall()
    print(f"{'ID':<4}{'No':<10}{'Airline':<15}{'From':<12}{'To':<12}{'Dep':<7}{'Arr':<7}{'Date':<12}{'Left':<6}{'Fare'}")
    print("-" * 95)
    for r in rows:
        print(f"{r[0]:<4}{r[1]:<10}{r[2]:<15}{r[3]:<12}{r[4]:<12}{r[5]:<7}{r[6]:<7}{str(r[7]):<12}{r[8]:<6}{r[9]}")
    con.close()


def search_by_route():
    con = _connect()
    cur = con.cursor()
    src = input("Source: ")
    dst = input("Destination: ")
    cur.execute("""
        SELECT flight_id, flight_no, airline, dep_time, arr_time, travel_date, seats_left, fare
        FROM flights WHERE source LIKE %s AND destination LIKE %s AND seats_left > 0
    """, (f"%{src}%", f"%{dst}%"))
    rows = cur.fetchall()
    if not rows:
        print("No flights found for this route.")
    for r in rows:
        print(f"ID {r[0]} | {r[1]} | {r[2]} | {r[3]}-{r[4]} | {r[5]} | Seats left: {r[6]} | Rs.{r[7]}")
    con.close()


def update_fare():
    con = _connect()
    cur = con.cursor()
    fid = int(input("Flight ID to update: "))
    fare = int(input("New Fare: "))
    cur.execute("UPDATE flights SET fare=%s WHERE flight_id=%s", (fare, fid))
    con.commit()
    print("Fare updated." if cur.rowcount else "Flight not found.")
    con.close()


def delete_flight():
    con = _connect()
    cur = con.cursor()
    fid = int(input("Flight ID to delete: "))
    cur.execute("DELETE FROM flights WHERE flight_id=%s", (fid,))
    con.commit()
    print("Flight deleted." if cur.rowcount else "Flight not found.")
    con.close()


def menu():
    while True:
        print("\n--- FLIGHTS ---")
        print("1. Add Flight")
        print("2. View All Flights")
        print("3. Search by Route (Source -> Destination)")
        print("4. Update Fare")
        print("5. Delete Flight")
        print("6. Back")
        ch = input("Choice: ")
        if ch == "1": add_flight()
        elif ch == "2": view_flights()
        elif ch == "3": search_by_route()
        elif ch == "4": update_fare()
        elif ch == "5": delete_flight()
        elif ch == "6": break
        else: print("Invalid choice.")
