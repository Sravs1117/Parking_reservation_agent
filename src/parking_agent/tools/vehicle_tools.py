import uuid
from ..db.client import connect

def verify_vehicle(plate_number: str) -> dict:
    """Verifies a vehicle by its license plate number against the records.

    Looks up the vehicle and its registered owner. Use this before doing
    anything else in a reservation flow, to confirm the vehicle is known
    and to find out its vehicle_type (needed to find a matching slot).

    Args:
        plate_number: The vehicle's license plate number, e.g. "KA01AB1234".

    Returns:
        A dict with status "found" and vehicle/owner details, or status
        "not_found" if no matching vehicle exists.
    """
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT v.vehicle_id, v.plate_number, v.vehicle_type, v.model,
                   e.employee_id, e.name AS owner_name, e.department
            FROM vehicles v
            JOIN employees e ON e.employee_id = v.owner_employee_id
            WHERE v.plate_number = ?
            """,
            (plate_number.strip().upper(),),
        ).fetchone()

        if row is not None:
            # Check if there is an active confirmed reservation for this vehicle
            active_res = conn.execute(
                """
                SELECT r.reservation_id, s.slot_number
                FROM reservations r
                JOIN parking_slots s ON s.slot_id = r.slot_id
                WHERE r.vehicle_id = ? AND r.status = 'confirmed'
                """,
                (row["vehicle_id"],)
            ).fetchone()
            
            if active_res is not None:
                return {
                    "status": "already_reserved",
                    "message": f"This vehicle already has an active reservation at slot {active_res['slot_number']}.",
                    "vehicle_id": row["vehicle_id"],
                    "plate_number": row["plate_number"],
                    "employee_id": row["employee_id"],
                    "slot_number": active_res["slot_number"]
                }
    finally:
        conn.close()

    if row is None:
        return {
            "status": "not_found",
            "message": f"No vehicle found with plate number '{plate_number}'. "
            "It can be registered with the register_vehicle tool before reserving a slot.",
        }

    return {
        "status": "found",
        "vehicle_id": row["vehicle_id"],
        "plate_number": row["plate_number"],
        "vehicle_type": row["vehicle_type"],
        "model": row["model"],
        "employee_id": row["employee_id"],
        "owner_name": row["owner_name"],
        "department": row["department"],
    }


def register_vehicle(
    plate_number: str, employee_id: str, vehicle_type: str, model: str = ""
) -> dict:
    """Registers a new vehicle for an employee when verification finds none.

    Args:
        plate_number: The vehicle's license plate number.
        employee_id: The employee ID of the vehicle's owner, e.g. "E001".
        vehicle_type: One of "car", "suv", "bike", "ev".
        model: Optional free-text vehicle model/make.

    Returns:
        A dict describing the newly created vehicle, or an error status.
    """
    vehicle_type = vehicle_type.strip().lower()
    if vehicle_type not in {"car", "suv", "bike", "ev"}:
        return {
            "status": "error",
            "message": f"Invalid vehicle_type '{vehicle_type}'. Must be one of car, suv, bike, ev.",
        }

    conn = connect()
    try:
        employee = conn.execute(
            "SELECT employee_id FROM employees WHERE employee_id = ?", (employee_id,)
        ).fetchone()
        if employee is None:
            return {"status": "error", "message": f"Unknown employee_id '{employee_id}'."}

        vehicle_id = f"V{uuid.uuid4().hex[:6].upper()}"
        conn.execute(
            "INSERT INTO vehicles (vehicle_id, plate_number, owner_employee_id, vehicle_type, model) "
            "VALUES (?, ?, ?, ?, ?)",
            (vehicle_id, plate_number.strip().upper(), employee_id, vehicle_type, model),
        )
        conn.commit()
    finally:
        conn.close()

    return {
        "status": "registered",
        "vehicle_id": vehicle_id,
        "plate_number": plate_number.strip().upper(),
        "vehicle_type": vehicle_type,
        "model": model,
        "employee_id": employee_id,
    }
