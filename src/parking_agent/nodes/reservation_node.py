import uuid
from datetime import datetime, timedelta, timezone
from typing import Any
from google.adk.events import Event
from ..db.client import connect

def save_reservation_or_cancel_node(node_input: Any, ctx):
    """Saves the reservation to the database on Yes, otherwise cancels."""
    details = ctx.state.get("temp_reservation", {})
    if not details or not details.get("slot_id"):
        return Event()

    user_reply = str(node_input).strip().lower() if node_input else ""

    if "yes" in user_reply:
        conn = connect()
        try:
            slot_id = details["slot_id"]
            slot = conn.execute("SELECT is_available FROM parking_slots WHERE slot_id = ?", (slot_id,)).fetchone()
            if slot is None or not slot["is_available"]:
                return Event(message=f"Slot '{details['slot_number']}' is no longer available.")

            start_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            end_time = (datetime.now(timezone.utc) + timedelta(hours=details["hours"])).isoformat().replace("+00:00", "Z")
            created_at = datetime.now(timezone.utc).isoformat()

            reservation_id = f"R{uuid.uuid4().hex[:8].upper()}"

            conn.execute(
                "INSERT INTO reservations "
                "(reservation_id, employee_id, vehicle_id, slot_id, start_time, end_time, hours, total_charge, status, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ?)",
                (reservation_id, details["employee_id"], details["vehicle_id"], slot_id, start_time, end_time, details["hours"], details["total_charge"], created_at),
            )
            conn.execute("UPDATE parking_slots SET is_available = 0 WHERE slot_id = ?", (slot_id,))
            conn.commit()
        finally:
            conn.close()

        return Event(
            message=f"Your parking reservation has been confirmed successfully. (Reservation ID: {reservation_id})",
            state={"reservation_result": {"status": "confirmed", "reservation_id": reservation_id}}
        )
    else:
        return Event(
            message="Reservation has been cancelled. No reservation was created.",
            state={"reservation_result": {"status": "cancelled"}}
        )
