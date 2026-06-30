-- Parking Reservation System schema

CREATE TABLE IF NOT EXISTS employees (
    employee_id     TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    department      TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id          TEXT PRIMARY KEY,
    plate_number        TEXT NOT NULL UNIQUE,
    owner_employee_id   TEXT NOT NULL,
    vehicle_type        TEXT NOT NULL CHECK (vehicle_type IN ('car', 'suv', 'bike', 'ev')),
    model               TEXT,
    FOREIGN KEY (owner_employee_id) REFERENCES employees (employee_id)
);

CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id         TEXT PRIMARY KEY,
    slot_number     TEXT NOT NULL UNIQUE,
    floor           TEXT NOT NULL,
    slot_type       TEXT NOT NULL CHECK (slot_type IN ('car', 'suv', 'bike', 'ev')),
    is_available    INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS rates (
    vehicle_type    TEXT PRIMARY KEY,
    hourly_rate     REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id  TEXT PRIMARY KEY,
    employee_id     TEXT NOT NULL,
    vehicle_id      TEXT NOT NULL,
    slot_id         TEXT NOT NULL,
    start_time      TEXT NOT NULL,
    end_time        TEXT NOT NULL,
    hours           REAL NOT NULL,
    total_charge    REAL NOT NULL,
    status          TEXT NOT NULL DEFAULT 'confirmed',
    created_at      TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
    FOREIGN KEY (slot_id) REFERENCES parking_slots (slot_id)
);
