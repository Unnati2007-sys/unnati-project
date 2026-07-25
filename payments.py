"""payments.py — Payment processing and collection reports.

Business rule: a payment ties to a booking. Modes: Card / UPI / NetBanking / Cash.
Status can be 'Success' or 'Pending'. Pending payments are highlighted in reports.
"""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="root", database="flight_2026")


def add_payment():
    con = _connect()
    cur = con.cursor()
    pay_id = int(input("Payment ID: "))
    bid = int(input("Booking ID: "))
    amount = int(input("Amount (Rs.): "))
    mode = input("Mode (Card/UPI/NetBanking/Cash): ")
    date = input("Payment Date (YYYY-MM-DD): ")
    status = input("Status (Success/Pending): ")
    cur.execute("INSERT INTO payments VALUES (%s,%s,%s,%s,%s,%s)",
                (pay_id, bid, amount, mode, date, status))
    con.commit()
    print("Payment recorded.")
    con.close()


def view_payments():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT pay.payment_id, pay.booking_id, p.name, pay.amount, pay.mode, pay.pay_date, pay.status
        FROM payments pay
        JOIN bookings b ON pay.booking_id = b.booking_id
        JOIN passengers p ON b.passenger_id = p.passenger_id
    """)
    rows = cur.fetchall()
    print(f"{'PID':<5}{'BID':<5}{'Passenger':<25}{'Amount':<10}{'Mode':<12}{'Date':<12}{'Status'}")
    print("-" * 85)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<5}{r[2]:<25}{r[3]:<10}{r[4]:<12}{str(r[5]):<12}{r[6]}")
    con.close()


def pending_payments():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT pay.payment_id, p.name, pay.amount, pay.pay_date
        FROM payments pay
        JOIN bookings b  ON pay.booking_id = b.booking_id
        JOIN passengers p ON b.passenger_id = p.passenger_id
        WHERE pay.status='Pending'
    """)
    rows = cur.fetchall()
    total = 0
    if not rows:
        print("No pending payments.")
    for r in rows:
        print(f"PID {r[0]} | {r[1]} | Rs.{r[2]} | {r[3]}")
        total += r[2]
    print(f"Total Pending: Rs.{total}")
    con.close()


def mark_success():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Payment ID to mark Success: "))
    cur.execute("UPDATE payments SET status='Success' WHERE payment_id=%s", (pid,))
    con.commit()
    print("Payment marked as Success." if cur.rowcount else "Payment not found.")
    con.close()


def revenue_summary():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT status, SUM(amount) FROM payments GROUP BY status")
    print("--- Revenue Summary ---")
    for status, total in cur.fetchall():
        print(f"{status}: Rs.{total}")
    con.close()


def menu():
    while True:
        print("\n--- PAYMENTS ---")
        print("1. Add Payment")
        print("2. View All Payments")
        print("3. View Pending Payments")
        print("4. Mark Payment as Success")
        print("5. Revenue Summary")
        print("6. Back")
        ch = input("Choice: ")
        if ch == "1": add_payment()
        elif ch == "2": view_payments()
        elif ch == "3": pending_payments()
        elif ch == "4": mark_success()
        elif ch == "5": revenue_summary()
        elif ch == "6": break
        else: print("Invalid choice.")
