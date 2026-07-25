"""blank_table.py — Initialize the flight_2026 database and all tables.

Run this ONCE before using the Flight Booking System.
Creates database `flight_2026` and the tables:
  - flights
  - passengers
  - bookings
  - payments
"""

import mysql.connector as sql


def create_database_and_tables():
    con = sql.connect(host="localhost", user="root", passwd="root")
    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS flight_2026")
    cur.execute("USE flight_2026")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id     INT PRIMARY KEY,
            flight_no     VARCHAR(10) NOT NULL,
            airline       VARCHAR(40),
            source        VARCHAR(30),
            destination   VARCHAR(30),
            dep_time      VARCHAR(10),
            arr_time      VARCHAR(10),
            travel_date   DATE,
            total_seats   INT,
            seats_left    INT,
            fare          INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id  INT PRIMARY KEY,
            name          VARCHAR(60) NOT NULL,
            age           INT,
            gender        VARCHAR(10),
            phone         VARCHAR(15),
            email         VARCHAR(60),
            passport_no   VARCHAR(15)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id    INT PRIMARY KEY,
            passenger_id  INT,
            flight_id     INT,
            seat_no       VARCHAR(5),
            booking_date  DATE,
            status        VARCHAR(15)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id    INT PRIMARY KEY,
            booking_id    INT,
            amount        INT,
            mode          VARCHAR(15),
            pay_date      DATE,
            status        VARCHAR(10)
        )
    """)

    con.commit()
    print("Database `flight_2026` and all tables created successfully.")
    cur.close()
    con.close()


if __name__ == "__main__":
    create_database_and_tables()
