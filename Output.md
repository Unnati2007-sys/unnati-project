# Output.md — Function reference with sample outputs

Sample outputs below assume the database has been seeded from `seed_data.sql`.

---

## `mainmenu.py`

### `mainmenu()`
Displays the top-level menu.
```
========= FLIGHT BOOKING SYSTEM =========
1. Flights
2. Passengers
3. Bookings
4. Payments
5. Graphs / Reports
6. Exit
Enter choice:
```

### `safe_call(func)`
Runs a module menu inside a try/except. On error:
```
[ERROR] mysql.connector.errors.IntegrityError: 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
Reason: The module could not complete due to the error above.

Restarting the program in 3 seconds...
```

### `restart_program()`
Uses `os.execl` to relaunch the app cleanly.

---

## `blank_table.py`

### `create_database_and_tables()`
```
Database `flight_2026` and all tables created successfully.
```

---

## `flights.py`

### `add_flight()`
```
Flight ID: 101
Flight No (e.g. AI-101): AI-505
Airline: Air India
Source city: Delhi
Destination city: Mumbai
Departure time (HH:MM): 09:30
Arrival time (HH:MM): 11:45
Travel Date (YYYY-MM-DD): 2026-09-15
Total Seats: 180
Fare (Rs.): 5500
Flight added successfully.
```

### `view_flights()`
```
ID  No        Airline        From        To          Dep    Arr    Date        Left  Fare
-----------------------------------------------------------------------------------------------
1   6E-234    IndiGo         Delhi       Mumbai      09:15  11:30  2026-03-11  145   4500
2   AI-108    Air India      Bengaluru   Delhi       17:45  20:15  2026-04-02  110   5500
...
```

### `search_by_route()`
```
Source: Delhi
Destination: Mumbai
ID 1 | 6E-234 | IndiGo | 09:15-11:30 | 2026-03-11 | Seats left: 145 | Rs.4500
ID 27 | AI-505 | Air India | 09:30-11:45 | 2026-09-15 | Seats left: 180 | Rs.5500
```

### `update_fare()`
```
Flight ID to update: 1
New Fare: 4800
Fare updated.
```

### `delete_flight()`
```
Flight ID to delete: 100
Flight deleted.
```

---

## `passengers.py`

### `add_passenger()`
```
Passenger ID: 11
Name: Rahul Sharma
Age: 29
Gender (M/F/O): M
Phone: 9876543210
Email: rahul.sharma@mail.com
Passport No: P1234567
Passenger added successfully.
```

### `view_passengers()`
```
ID   Name                     Age  Gender  Phone          Passport
---------------------------------------------------------------------------
1    Aarav Sharma             27   M       9123456789     P1234567
2    Diya Verma               34   F       9234567890     P2345678
...
```

### `search_passenger()`
```
Passenger ID: 1
ID: 1
Name: Aarav Sharma
Age: 27
Gender: M
Phone: 9123456789
Email: aarav.sharma@mail.com
Passport: P1234567
```

### `update_passenger()`
```
Passenger ID: 1
New Phone: 9999999999
New Email: aarav.new@mail.com
Passenger updated.
```

### `delete_passenger()`
```
Passenger ID: 11
Passenger deleted.
```

---

## `bookings.py`

### `book_ticket()`
Refuses if the flight is full; otherwise decrements `seats_left`.
```
Booking ID: 31
Passenger ID: 5
Flight ID: 12
Seat No (e.g. 12A): 14C
Booking 31 confirmed on seat 14C.
```
If full:
```
Sorry, this flight is fully booked.
```

### `view_bookings()`
```
BID  Passenger                Flight    Route                    Date        Seat  Status
-----------------------------------------------------------------------------------------------
1    Aarav Sharma             6E-234    Delhi->Mumbai            2026-03-11  12A   Confirmed
2    Diya Verma               AI-108    Bengaluru->Delhi         2026-04-02  8B    Cancelled
...
```

### `cancel_booking()`
```
Booking ID to cancel: 1
Booking cancelled and seat released.
```

### `bookings_by_passenger()`
```
Passenger ID: 3
BID 7 | 6E-501 | Delhi->Goa | 2026-05-14 | Seat 21D | Confirmed
BID 22 | UK-880 | Mumbai->Hyderabad | 2026-08-03 | Seat 4A | Cancelled
```

---

## `payments.py`

### `add_payment()`
```
Payment ID: 31
Booking ID: 31
Amount (Rs.): 5500
Mode (Card/UPI/NetBanking/Cash): UPI
Payment Date (YYYY-MM-DD): 2026-09-10
Status (Success/Pending): Success
Payment recorded.
```

### `view_payments()`
```
PID  BID  Passenger                Amount    Mode        Date        Status
-------------------------------------------------------------------------------------
1    1    Aarav Sharma             4500      UPI         2026-03-11  Success
2    2    Diya Verma               5500      Card        2026-04-02  Pending
...
```

### `pending_payments()`
```
PID 2 | Diya Verma | Rs.5500 | 2026-04-02
PID 9 | Ishaan Singh | Rs.6500 | 2026-07-18
Total Pending: Rs.12000
```

### `mark_success()`
```
Payment ID to mark Success: 2
Payment marked as Success.
```

### `revenue_summary()`
```
--- Revenue Summary ---
Success: Rs.145000
Pending: Rs.24000
```

---

## `graphs.py`

### `flights_by_airline()`
Opens a bar chart with one bar per airline (IndiGo, Air India, SpiceJet, Vistara, GoAir, Akasa Air) showing flight counts.

### `booking_status_chart()`
Opens a pie chart of Confirmed vs Cancelled proportions, e.g. `Confirmed: 75.0% | Cancelled: 25.0%`.

### `top_routes()`
Opens a bar chart of the 5 most-booked routes by confirmed bookings, e.g. `Delhi->Mumbai`, `Bengaluru->Delhi`, etc.

### `revenue_by_mode()`
Opens a pie chart of successful revenue grouped by payment mode (Card / UPI / NetBanking / Cash).

---

_Created for SRM CEM Lucknow._
