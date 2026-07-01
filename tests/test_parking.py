import os
import sys

# Add 'src' to system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from parking_agent.tools.vehicle_tools import verify_vehicle
from parking_agent.tools.slot_tools import find_available_slots
from parking_agent.tools.price_tools import calculate_parking_charge
from parking_agent.workflows.workflow import root_agent

def test_workflow_loads():
    """Verify that the ADK workflow initializes and loads successfully."""
    assert root_agent is not None
    assert root_agent.name == "parking_reservation_pipeline"

def test_verify_vehicle():
    """Test vehicle verification tool logic."""
    # Test a registered vehicle (e.g., KA03EF9012)
    res = verify_vehicle("KA03EF9012")
    assert res["status"] == "found"
    assert res["vehicle_type"].lower() == "suv"

    # Test an unregistered vehicle
    res_unknown = verify_vehicle("XYZ9999")
    assert res_unknown["status"] == "not_found"

def test_calculate_parking_charge():
    """Test reservation pricing calculation rules."""
    # SUV rate is 45.0/hour. 2 hours should be 90.0
    res = calculate_parking_charge("suv", 2.0)
    assert res["status"] == "ok"
    assert res["total_charge"] == 90.0

    # Billing rounds to the nearest 30 mins: 1.2 hours -> 1.0 hour billable
    res_round = calculate_parking_charge("suv", 1.2)
    assert res_round["status"] == "ok"
    assert res_round["billable_hours"] == 1.0
    assert res_round["total_charge"] == 45.0

def test_find_available_slots():
    """Test slot search query filters."""
    res = find_available_slots("suv", floor="1")
    assert res["status"] == "ok"
    assert "available_slots" in res
    assert len(res["available_slots"]) > 0

if __name__ == "__main__":
    print("Executing tests...")
    test_workflow_loads()
    print("[OK] test_workflow_loads passed")
    test_verify_vehicle()
    print("[OK] test_verify_vehicle passed")
    test_calculate_parking_charge()
    print("[OK] test_calculate_parking_charge passed")
    test_find_available_slots()
    print("[OK] test_find_available_slots passed")
    print("All tests passed successfully!")
