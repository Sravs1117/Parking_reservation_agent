import uuid
from datetime import datetime, timezone
from google.adk.tools.tool_context import ToolContext
from ..db.client import connect

def save_reservation(
    employee_id: str,
    vehicle_id: str,
    slot_id: str,
    start_time: str,
    end_time: str,
    hours: float,
    total_charge: float,
    tool_context: ToolContext,
) -> dict:
    """Saves a confirmed parking reservation and marks the slot as occupied.

    IMPORTANT: This tool requires explicit human confirmation before it
    executes (configured via require_confirmation=True). Only call it after
    you have shown the employee a full summary of the vehicle, slot, time
    window, and total charge, and they have agreed to proceed.

    Args:
        employee_id: The employee making the reservation, e.g. "E001".
        vehicle_id: The verified/registered vehicle_id, e.g. "V001".
        slot_id: The chosen slot_id from find_available_slots, e.g. "S001".
        start_time: ISO-8601 start time of the reservation.
        end_time: ISO-8601 end time of the reservation.
        hours: Duration of the reservation in hours.
        total_charge: The final charge computed by calculate_parking_charge.
        tool_context: Injected automatically by ADK; do not set manually.

    Returns:
        A dict describing the saved reservation, or an error if the slot
        is no longer available.
    """
    conn = connect()
    try:
        slot = conn.execute(
            "SELECT is_available FROM parking_slots WHERE slot_id = ?", (slot_id,)
        ).fetchone()
        if slot is None:
            return {"status": "error", "message": f"Unknown slot_id '{slot_id}'."}
        if not slot["is_available"]:
            return {"status": "error", "message": f"Slot '{slot_id}' is no longer available. Please pick another."}

        # Check for duplicate bookings
        existing = conn.execute(
            "SELECT reservation_id, slot_id FROM reservations "
            "WHERE vehicle_id = ? AND start_time = ? AND status = 'confirmed'",
            (vehicle_id, start_time)
        ).fetchone()
        if existing:
            return {
                "status": "already_booked",
                "message": f"Vehicle is already booked at this time for slot '{existing['slot_id']}'. Reservation ID: {existing['reservation_id']}"
            }

        reservation_id = f"R{uuid.uuid4().hex[:8].upper()}"
        created_at = datetime.now(timezone.utc).isoformat()

        conn.execute(
            "INSERT INTO reservations "
            "(reservation_id, employee_id, vehicle_id, slot_id, start_time, end_time, hours, total_charge, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ?)",
            (reservation_id, employee_id, vehicle_id, slot_id, start_time, end_time, hours, total_charge, created_at),
        )
        conn.execute("UPDATE parking_slots SET is_available = 0 WHERE slot_id = ?", (slot_id,))
        conn.commit()
    finally:
        conn.close()

    return {
        "status": "confirmed",
        "reservation_id": reservation_id,
        "employee_id": employee_id,
        "vehicle_id": vehicle_id,
        "slot_id": slot_id,
        "start_time": start_time,
        "end_time": end_time,
        "hours": hours,
        "total_charge": total_charge,
        "created_at": created_at,
    }
