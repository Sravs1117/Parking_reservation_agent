from google.adk.agents import LlmAgent
from ..config import settings
from ..tools.price_tools import calculate_parking_charge
from ..prompts import PRICING_PROMPT

charge_calculator_agent = LlmAgent(
    name="charge_calculator_agent",
    model=settings.MODEL,
    description="Calculates the parking fee for the reservation.",
    instruction=PRICING_PROMPT,
    tools=[calculate_parking_charge],
    output_key="charge_info",
)
