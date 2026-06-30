from google.adk import Workflow
from google.adk.workflow import JoinNode

from ..nodes import (
    save_user_request,
    router_agent,
    route_parser,
    vehicle_verification_agent,
    verification_router,
    proceed_to_parallel_tasks,
    end_verification_flow,
    slot_finder_agent,
    charge_calculator_agent,
    display_summary_and_ask_node,
    save_reservation_or_cancel_node,
)

join_node = JoinNode(name="join_node")

root_agent = Workflow(
    name="parking_reservation_pipeline",
    description="End-to-end employee parking reservation pipeline using a Graph Workflow.",
    edges=[
        ("START", save_user_request, router_agent, route_parser, {
            "FULL_FLOW": vehicle_verification_agent,
            "CHECK_SLOTS": slot_finder_agent,
            "CHECK_PRICE": charge_calculator_agent
        }),
        (vehicle_verification_agent, verification_router, {
            "PROCEED": proceed_to_parallel_tasks,
            "STOP": end_verification_flow
        }),
        (proceed_to_parallel_tasks, (slot_finder_agent, charge_calculator_agent)),
        (slot_finder_agent, join_node),
        (charge_calculator_agent, join_node),
        (join_node, display_summary_and_ask_node, save_reservation_or_cancel_node)
    ],
)
