"""
Initializes the SQLite database for the Parking Reservation System.

Usage:
    python scripts/seed_parking_db.py
    python scripts/seed_parking_db.py --reset      # drop & recreate everything
    python scripts/seed_parking_db.py --db-path /custom/path/parking.db
"""

import argparse
import os
import sqlite3
from datetime import datetime, timezone

# Locate DB files relative to the scripts/ folder
DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "parking.db"))
SCHEMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "schema.sql"))


def init_db(db_path: str, reset: bool = False) -> None:
    if reset and os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cur.executescript(f.read())

    # --- Seed: employees ---
    employees = [
        ("E001", "Asha Rao", "Engineering"),
        ("E002", "Vikram Shah", "Sales"),
        ("E003", "Priya Nair", "HR"),
        ("E004", "Karthik Menon", "Engineering"),
        ("E005", "Rohan Verma", "Marketing"),
        ("E006", "Ananya Sen", "Finance"),
        ("E007", "Suresh Kumar", "Operations"),
        ("E008", "Meera Patel", "Engineering"),
        ("E009", "Kabir Singh", "Sales"),
        ("E010", "Divya Nair", "HR"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO employees (employee_id, name, department) VALUES (?, ?, ?)",
        employees,
    )

    # --- Seed: vehicles ---
    vehicles = [
        ("V001", "KA01AB1234", "E001", "car", "Honda City"),
        ("V002", "KA02CD5678", "E002", "bike", "Royal Enfield Classic"),
        ("V003", "KA03EF9012", "E003", "suv", "Mahindra XUV700"),
        ("V004", "KA04GH3456", "E004", "ev", "Tata Nexon EV"),
        ("V005", "KA05JK7890", "E005", "car", "Maruti Swift"),
        ("V006", "KA06LM1234", "E006", "bike", "Honda Activa"),
        ("V007", "KA07NP5678", "E007", "suv", "Hyundai Creta"),
        ("V008", "KA08QR9012", "E008", "ev", "MG ZS EV"),
        ("V009", "KA09ST3456", "E009", "car", "Hyundai i20"),
        ("V010", "KA10UV7890", "E010", "suv", "Tata Safari"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO vehicles (vehicle_id, plate_number, owner_employee_id, vehicle_type, model) "
        "VALUES (?, ?, ?, ?, ?)",
        vehicles,
    )

    # --- Seed: parking slots ---
    slots = []
    floor_plan = {
        "1": [("car", 6), ("suv", 2)],
        "2": [("bike", 8), ("ev", 2)],
    }
    counter = 1
    for floor, groups in floor_plan.items():
        for slot_type, count in groups:
            for _ in range(count):
                slot_id = f"S{counter:03d}"
                slot_number = f"{floor}-{slot_type.upper()}-{counter:03d}"
                slots.append((slot_id, slot_number, floor, slot_type, 1))
                counter += 1
    cur.executemany(
        "INSERT OR IGNORE INTO parking_slots (slot_id, slot_number, floor, slot_type, is_available) "
        "VALUES (?, ?, ?, ?, ?)",
        slots,
    )

    # --- Seed: hourly rates ---
    rates = [
        ("car", 30.0),
        ("suv", 45.0),
        ("bike", 10.0),
        ("ev", 25.0),  # discounted rate to encourage EV usage
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO rates (vehicle_type, hourly_rate) VALUES (?, ?)",
        rates,
    )

    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path}")
    print(f"  employees: {len(employees)}, vehicles: {len(vehicles)}, "
          f"slots: {len(slots)}, rate tiers: {len(rates)}")
    print(f"  timestamp: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the parking system database.")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="Path to the SQLite database file.")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate the database.")
    args = parser.parse_args()
    init_db(args.db_path, reset=args.reset)
