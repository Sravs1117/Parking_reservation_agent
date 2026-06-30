import re
from typing import Any
from google.adk.events import Event, RequestInput
from ..db.client import connect

def save_user_request(node_input: str):
    """Saves the user request and clears execution states for any new turn."""
    return Event(
        output=node_input,
        state={
            "user_request": node_input,
            "vehicle_info": None,
            "slot_options": None,
            "charge_info": None,
            "temp_reservation": None,
            "reservation_result": None
        }
    )


def parse_reservation_details(ctx) -> dict:
    """Parses agent outputs and queries the database to extract complete details."""
    vehicle_info = ctx.state.get("vehicle_info", "")
    slot_options = ctx.state.get("slot_options", "")
    charge_info = ctx.state.get("charge_info", "")

    # Extract plate
    plate_match = re.search(r"\(([A-Z0-9]+)\)", vehicle_info)
    plate = plate_match.group(1) if plate_match else ""
    if not plate:
        plate_match = re.search(r"\b([A-Z]{2}\d{2}[A-Z]{1,2}\d{4})\b", vehicle_info, re.IGNORECASE)
        plate = plate_match.group(1) if plate_match else ""

    # Extract slot ID
    slot_id_match = re.search(r"slot_id\s+([A-Z0-9]+)", slot_options, re.IGNORECASE)
    slot_id = slot_id_match.group(1) if slot_id_match else ""
    if not slot_id:
        slot_id_match = re.search(r"\b(S\d{3})\b", slot_options, re.IGNORECASE)
        slot_id = slot_id_match.group(1) if slot_id_match else ""

    # Extract floor
    floor_match = re.search(r"floor\s+(\d+)", slot_options, re.IGNORECASE)
    floor = floor_match.group(1) if floor_match else ""

    # Extract duration
    duration_match = re.search(r"(\d+(?:\.\d+)?)\s*hours?", charge_info, re.IGNORECASE)
    duration = float(duration_match.group(1)) if duration_match else 3.0

    # Extract charge
    charge_match = re.search(r"(\d+(?:\.\d+)?)\s*INR", charge_info, re.IGNORECASE)
    if not charge_match:
        charge_match = re.search(r"\$\s*(\d+(?:\.\d+)?)", charge_info)
    if not charge_match:
        charge_match = re.search(r"(?:price|charge|be|is)\s+(?:\$\s*)?(\d+(?:\.\d+)?)", charge_info, re.IGNORECASE)
    if not charge_match:
        charge_match = re.search(r"(\d+(?:\.\d+)?)", charge_info)
    total_charge = float(charge_match.group(1)) if charge_match else 0.0

    # Query DB to get actual database IDs and details
    vehicle_id = ""
    employee_id = ""
    slot_number = ""
    
    conn = connect()
    try:
        if plate:
            veh = conn.execute(
                "SELECT vehicle_id, owner_employee_id FROM vehicles WHERE plate_number = ?",
                (plate.upper(),)
            ).fetchone()
            if veh:
                vehicle_id = veh["vehicle_id"]
                employee_id = veh["owner_employee_id"]
        
        if slot_id:
            slot = conn.execute(
                "SELECT slot_number, floor FROM parking_slots WHERE slot_id = ?",
                (slot_id.upper(),)
            ).fetchone()
            if slot:
                slot_number = slot["slot_number"]
                floor = slot["floor"]
    finally:
        conn.close()

    return {
        "plate_number": plate.upper(),
        "employee_id": employee_id,
        "vehicle_id": vehicle_id,
        "slot_id": slot_id,
        "slot_number": slot_number,
        "floor": floor,
        "duration": f"{duration} hours",
        "hours": duration,
        "total_charge": total_charge
    }


async def display_summary_and_ask_node(node_input: Any, ctx):
    """Displays reservation details and prompts for human confirmation."""
    vehicle_info = ctx.state.get("vehicle_info")
    slot_options = ctx.state.get("slot_options")
    charge_info = ctx.state.get("charge_info")

    if not vehicle_info or not slot_options or not charge_info:
        return

    details = parse_reservation_details(ctx)
    
    if not details.get("slot_id"):
        yield Event(message="I'm sorry, no available slots were found. The reservation cannot be completed.")
        return

    summary_message = f"""Reservation Summary:
- Vehicle Number: {details['plate_number']}
- Employee ID: {details['employee_id']}
- Parking Slot: {details['slot_number']}
- Floor: {details['floor']}
- Duration: {details['duration']}
- Total Parking Charge: {details['total_charge']} INR

Would you like to confirm this reservation? Reply Yes to confirm or No to cancel."""

    yield Event(state={"temp_reservation": details})
    yield RequestInput(message=summary_message)
