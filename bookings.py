"""bookings.py — Ticket booking, cancellation, and lookup.

Business rules:
- Booking decrements the flight's seats_left; cancellation increments it back.
- Booking is refused if seats_left is 0.
- Cancelling a booking sets its status to 'Cancelled' but keeps the record.
"""

import mysql.connector as sql
from datetime import date


def _connect():
    return sql.connect(host="localhost", user="root", passwd="root", database="flight_2026")


def book_ticket():
    con = _connect()
    cur = con.cursor()
    bid = int(input("Booking ID: "))
    pid = int(input("Passenger ID: "))
    fid = int(input("Flight ID: "))

    cur.execute("SELECT seats_left FROM flights WHERE flight_id=%s", (fid,))
    r = cur.fetchone()
    if not r:
        print("Flight not found.")
        con.close()
        return
    if r[0] <= 0:
        print("Sorry, this flight is fully booked.")
        con.close()
        return

    seat_no = input("Seat No (e.g. 12A): ")
    cur.execute("INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s)",
                (bid, pid, fid, seat_no, date.today().isoformat(), "Confirmed"))
    cur.execute("UPDATE flights SET seats_left = seats_left - 1 WHERE flight_id=%s", (fid,))
    con.commit()
    print(f"Booking {bid} confirmed on seat {seat_no}.")
    con.close()


def view_bookings():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT b.booking_id, p.name, f.flight_no, f.source, f.destination,
               f.travel_date, b.seat_no, b.status
        FROM bookings b
        JOIN passengers p ON b.passenger_id = p.passenger_id
        JOIN flights   f ON b.flight_id    = f.flight_id
        ORDER BY b.booking_id
    """)
    rows = cur.fetchall()
    print(f"{'BID':<5}{'Passenger':<25}{'Flight':<10}{'Route':<25}{'Date':<12}{'Seat':<6}{'Status'}")
    print("-" * 95)
    for r in rows:
        route = f"{r[3]}->{r[4]}"
        print(f"{r[0]:<5}{r[1]:<25}{r[2]:<10}{route:<25}{str(r[5]):<12}{r[6]:<6}{r[7]}")
    con.close()


def cancel_booking():
    con = _connect()
    cur = con.cursor()
    bid = int(input("Booking ID to cancel: "))
    cur.execute("SELECT flight_id, status FROM bookings WHERE booking_id=%s", (bid,))
    r = cur.fetchone()
    if not r:
        print("Booking not found.")
        con.close()
        return
    if r[1] == "Cancelled":
        print("This booking is already cancelled.")
        con.close()
        return
    cur.execute("UPDATE bookings SET status='Cancelled' WHERE booking_id=%s", (bid,))
    cur.execute("UPDATE flights SET seats_left = seats_left + 1 WHERE flight_id=%s", (r[0],))
    con.commit()
    print("Booking cancelled and seat released.")
    con.close()


def bookings_by_passenger():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Passenger ID: "))
    cur.execute("""
        SELECT b.booking_id, f.flight_no, f.source, f.destination,
               f.travel_date, b.seat_no, b.status
        FROM bookings b JOIN flights f ON b.flight_id=f.flight_id
        WHERE b.passenger_id=%s
    """, (pid,))
    rows = cur.fetchall()
    if not rows:
        print("No bookings for this passenger.")
    for r in rows:
        print(f"BID {r[0]} | {r[1]} | {r[2]}->{r[3]} | {r[4]} | Seat {r[5]} | {r[6]}")
    con.close()


def menu():
    while True:
        print("\n--- BOOKINGS ---")
        print("1. Book a Ticket")
        print("2. View All Bookings")
        print("3. Cancel a Booking")
        print("4. View Bookings by Passenger")
        print("5. Back")
        ch = input("Choice: ")
        if ch == "1": book_ticket()
        elif ch == "2": view_bookings()
        elif ch == "3": cancel_booking()
        elif ch == "4": bookings_by_passenger()
        elif ch == "5": break
        else: print("Invalid choice.")
