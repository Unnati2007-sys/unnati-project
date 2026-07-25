"""graphs.py — Visualizations for flight booking data using matplotlib."""

import mysql.connector as sql
import matplotlib.pyplot as plt


def _connect():
    return sql.connect(host="localhost", user="root", passwd="root", database="flight_2026")


def flights_by_airline():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT airline, COUNT(*) FROM flights GROUP BY airline")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    counts = [d[1] for d in data]
    plt.bar(labels, counts, color="skyblue")
    plt.title("Flights per Airline")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    con.close()


def booking_status_chart():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT status, COUNT(*) FROM bookings GROUP BY status")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    counts = [d[1] for d in data]
    plt.pie(counts, labels=labels, autopct="%1.1f%%")
    plt.title("Booking Status")
    plt.show()
    con.close()


def top_routes():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT CONCAT(f.source,'->',f.destination) AS route, COUNT(*) AS cnt
        FROM bookings b JOIN flights f ON b.flight_id=f.flight_id
        WHERE b.status='Confirmed'
        GROUP BY route ORDER BY cnt DESC LIMIT 5
    """)
    data = cur.fetchall()
    labels = [d[0] for d in data]
    counts = [d[1] for d in data]
    plt.bar(labels, counts, color="orange")
    plt.title("Top 5 Routes by Confirmed Bookings")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    con.close()


def revenue_by_mode():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT mode, SUM(amount) FROM payments WHERE status='Success' GROUP BY mode")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    totals = [d[1] for d in data]
    plt.pie(totals, labels=labels, autopct="%1.1f%%")
    plt.title("Revenue by Payment Mode")
    plt.show()
    con.close()


def menu():
    while True:
        print("\n--- GRAPHS ---")
        print("1. Flights per Airline (Bar)")
        print("2. Booking Status (Pie)")
        print("3. Top 5 Routes (Bar)")
        print("4. Revenue by Payment Mode (Pie)")
        print("5. Back")
        ch = input("Choice: ")
        if ch == "1": flights_by_airline()
        elif ch == "2": booking_status_chart()
        elif ch == "3": top_routes()
        elif ch == "4": revenue_by_mode()
        elif ch == "5": break
        else: print("Invalid choice.")
