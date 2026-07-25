# StepToCreate.md — Logic behind the Flight Booking System

This document explains the reasoning and creation order behind every file. Follow the steps top-to-bottom to build a similar system from scratch.

## Step 1 — Identify the domain entities

An airline booking workflow revolves around four core entities:

1. **Flights** — scheduled trips with a route, timing, seat count, and fare
2. **Passengers** — the travellers who book tickets
3. **Bookings** — the reservation linking a passenger to a flight and a seat
4. **Payments** — the money side: what was collected for each booking

Everything else (reports, graphs) is derived from these four.

## Step 2 — Design the database schema

- `flights(flight_id PK, flight_no, airline, source, destination, dep_time, arr_time, travel_date, total_seats, seats_left, fare)`
  - `seats_left` is the key inventory counter — kept live so we do not have to `COUNT(*)` bookings on every search.
- `passengers(passenger_id PK, name, age, gender, phone, email, passport_no)`
- `bookings(booking_id PK, passenger_id, flight_id, seat_no, booking_date, status)`
- `payments(payment_id PK, booking_id, amount, mode, pay_date, status)`

## Step 3 — Create `blank_table.py`

A one-shot bootstrap script that creates the `flight_2026` database and all four tables with `CREATE TABLE IF NOT EXISTS`. A new user can spin up the entire schema by running one file — no manual SQL required.

## Step 4 — Build each functional module

Each module follows the same shape: a private `_connect()`, feature functions, and a `menu()` loop.

### `flights.py`
Standard CRUD plus a **route search** (`WHERE source LIKE %s AND destination LIKE %s AND seats_left > 0`). The `seats_left > 0` guard hides sold-out flights.

### `passengers.py`
Standard CRUD. Update focuses on phone/email because those change most often.

### `bookings.py`
Two business rules make this module non-trivial:

- **Book** — read `seats_left`, refuse if 0, insert booking, then `UPDATE flights SET seats_left = seats_left - 1`.
- **Cancel** — mark booking `Cancelled` (do NOT delete, we keep the audit trail) and increment `seats_left` back.

This shows how transactional logic protects the flight's inventory.

### `payments.py`
Bills for a booking with a mode (Card / UPI / NetBanking / Cash) and a status. `pending_payments()` sums outstanding dues, `revenue_summary()` groups by status.

### `graphs.py`
Matplotlib charts derived directly from `GROUP BY` queries — flights per airline, booking status, top 5 routes (JOIN + `LIMIT 5`), revenue by payment mode.

## Step 5 — Wire up `mainmenu.py`

The main menu imports all module files and dispatches based on the user's numeric choice.

- **`safe_call(func)`** wraps any module call. If the module raises, it prints the error class and message, then calls `restart_program()`.
- **`restart_program()`** uses `os.execl(sys.executable, sys.executable, *sys.argv)` to relaunch the same script cleanly, after a 3-second delay so the user can read the error.
- Non-numeric input is rejected via `str.isdigit()` before conversion.

## Step 6 — Seed data (`seed_data.sql`)

Reproducible sample data drives the demo:
- 100 flights across 6 airlines and 10 Indian cities
- 10 passengers with contact info and passport numbers
- ~30 bookings with mixed Confirmed / Cancelled statuses
- ~30 payments across 4 modes with a 3:1 Success:Pending ratio

## Step 7 — Documentation

- **`README.md`** — install + run instructions and feature list
- **`StepToCreate.md`** — this file (the "why")
- **`Output.md`** — what each function does and a sample output

## Recommended creation order

1. `blank_table.py` (schema)
2. `flights.py`, `passengers.py` (base data)
3. `bookings.py`, `payments.py` (transactional data with business rules)
4. `graphs.py` (reporting)
5. `mainmenu.py` (glue + error handling)
6. `seed_data.sql`
7. Docs (`README`, `StepToCreate`, `Output`)

---

_Created for SRM CEM Lucknow._
