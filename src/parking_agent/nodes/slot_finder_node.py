from google.adk.agents import LlmAgent
from ..config import settings
from ..tools.slot_tools import find_available_slots
from ..prompts import SLOT_FINDER_PROMPT

slot_finder_agent = LlmAgent(
    name="slot_finder_agent",
    model=settings.MODEL,
    description="Finds available parking slots matching the vehicle type.",
    instruction=SLOT_FINDER_PROMPT,
    tools=[find_available_slots],
    output_key="slot_options",
)
