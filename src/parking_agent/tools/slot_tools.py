from ..db.client import connect

def find_available_slots(vehicle_type: str, floor: str = "") -> dict:
    """Finds available parking slots matching a vehicle type.

    Args:
        vehicle_type: One of "car", "suv", "bike", "ev".
        floor: Optional floor filter, e.g. "1" or "2". Leave empty for any floor.

    Returns:
        A dict with status and a list of available slots (slot_id, slot_number, floor).
    """
    vehicle_type = vehicle_type.strip().lower()
    conn = connect()
    try:
        query = "SELECT slot_id, slot_number, floor FROM parking_slots WHERE slot_type = ? AND is_available = 1"
        params = [vehicle_type]
        if floor:
            query += " AND floor = ?"
            params.append(floor)
        query += " ORDER BY slot_number LIMIT 10"
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    if not rows:
        return {
            "status": "none_available",
            "vehicle_type": vehicle_type,
            "message": f"No available slots currently match vehicle_type '{vehicle_type}'.",
        }

    return {
        "status": "ok",
        "vehicle_type": vehicle_type,
        "available_slots": [
            {"slot_id": r["slot_id"], "slot_number": r["slot_number"], "floor": r["floor"]} for r in rows
        ],
    }
