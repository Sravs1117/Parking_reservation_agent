from typing import Any
from google.adk.agents import LlmAgent
from google.adk.events import Event
from ..config import settings
from ..tools.vehicle_tools import verify_vehicle
from ..prompts import VERIFICATION_PROMPT

vehicle_verification_agent = LlmAgent(
    name="vehicle_verification_agent",
    model=settings.MODEL,
    description="Verifies an employee's vehicle by plate number.",
    instruction=VERIFICATION_PROMPT,
    tools=[verify_vehicle],
    output_key="vehicle_info",
)

def verification_router(node_input: str):
    if "Verified vehicle" in node_input:
        return Event(route="PROCEED")
    return Event(route="STOP")

def end_verification_flow(node_input: Any):
    return Event()

def proceed_to_parallel_tasks(node_input: Any):
    return node_input
