# Flight Booking System

A Python + MySQL based Flight Booking System with a modular architecture. Handles flights, passengers, bookings, payments, and visual reports — with graceful error handling and auto-restart in the main menu.

## Features

1. **Flights** — Add, view, and delete flights; search by source/destination route; update fare.
2. **Passengers** — Register passengers with contact info + passport, and manage profiles.
3. **Bookings** — Book tickets (auto seat decrement + full-flight check), cancel bookings (seat released back), and view bookings per passenger.
4. **Payments** — Record payments per booking, list pending payments with totals, mark payments as Success, and view revenue summary.
5. **Graphs / Reports** — Matplotlib charts:
   - Flights per airline (bar)
   - Booking status distribution (pie)
   - Top 5 routes by confirmed bookings (bar)
   - Revenue by payment mode (pie)
6. **Error handling & auto-restart** — Every module call is wrapped in `safe_call`. On error, the program prints the reason and auto-restarts after 3 seconds.

## Project Structure

```
flight_booking_system/
├── mainmenu.py        # Central menu with error handling & auto-restart
├── blank_table.py     # Creates the flight_2026 DB and all tables
├── flights.py         # Flight schedule CRUD + route search
├── passengers.py      # Passenger CRUD
├── bookings.py        # Ticket booking, cancellation, lookups
├── payments.py        # Payments, pending list, revenue summary
├── graphs.py          # Matplotlib visualizations
├── seed_data.sql      # 100 flights, 10 passengers, ~30 bookings, ~30 payments
├── README.md
├── StepToCreate.md
└── Output.md
```

## Database Schema

Database: **`flight_2026`**

| Table | Columns |
|-------|---------|
| `flights` | flight_id, flight_no, airline, source, destination, dep_time, arr_time, travel_date, total_seats, seats_left, fare |
| `passengers` | passenger_id, name, age, gender, phone, email, passport_no |
| `bookings` | booking_id, passenger_id, flight_id, seat_no, booking_date, status |
| `payments` | payment_id, booking_id, amount, mode, pay_date, status |

## Setup

1. Install MySQL Server and set the root password to `root` (or edit `_connect()` in each module).
2. Install Python dependencies:
   ```sh
   pip install mysql-connector-python matplotlib
   ```
3. Create the database and tables:
   ```sh
   python blank_table.py
   ```
4. Load the seed data:
   ```sh
   mysql -u root -p flight_2026 < seed_data.sql
   ```
5. Run the application:
   ```sh
   python mainmenu.py
   ```

## Sample Data

- **100 flights** across 6 airlines and 10 Indian cities
- **10 passengers** with contact info and passport numbers
- **~30 bookings** with mixed Confirmed / Cancelled statuses
- **~30 payments** across 4 payment modes

## Business Rules

- **Booking** decrements `seats_left`; refuses when it reaches 0.
- **Cancellation** releases the seat back to the flight's inventory.
- **Route search** ignores flights with `seats_left = 0`.

---

_Created for SRM CEM Lucknow._
