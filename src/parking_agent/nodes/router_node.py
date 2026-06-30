from google.adk.agents import LlmAgent
from google.adk.events import Event
from ..config import settings
from ..prompts import ROUTER_PROMPT

router_agent = LlmAgent(
    name="router_agent",
    model=settings.MODEL,
    description="Routes the user's request to the appropriate sub-agent.",
    instruction=ROUTER_PROMPT,
    output_schema=str
)

def route_parser(node_input: str):
    route = node_input.strip().strip('"\'')
    return Event(route=route, state={"active_route": route})
