from ..db.client import connect

def calculate_parking_charge(vehicle_type: str, hours: float) -> dict:
    """Calculates the parking charge for a vehicle type and duration.

    Args:
        vehicle_type: One of "car", "suv", "bike", "ev".
        hours: Number of hours the reservation will last (can be fractional, e.g. 2.5).

    Returns:
        A dict with the hourly_rate, hours, and computed total_charge, or an
        error status if the vehicle type has no configured rate.
    """
    vehicle_type = vehicle_type.strip().lower()
    if hours <= 0:
        return {"status": "error", "message": "hours must be a positive number."}

    conn = connect()
    try:
        row = conn.execute(
            "SELECT hourly_rate FROM rates WHERE vehicle_type = ?", (vehicle_type,)
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return {"status": "error", "message": f"No rate configured for vehicle_type '{vehicle_type}'."}

    hourly_rate = row["hourly_rate"]
    # Billed in 30-minute increments, rounded up.
    billable_hours = max(0.5, round(hours * 2) / 2)
    total_charge = round(hourly_rate * billable_hours, 2)

    return {
        "status": "ok",
        "vehicle_type": vehicle_type,
        "hourly_rate": hourly_rate,
        "hours_requested": hours,
        "billable_hours": billable_hours,
        "total_charge": total_charge,
    }
