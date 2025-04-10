from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.nodes.create_itinerary import create_itinerary
from agent.nodes.extract_preferences import extract_preferences
from agent.nodes.find_destinations import find_destinations
from agent.nodes.handle_followup import handle_followup
from agent.state import AgentState


# Build graph
def build_travel_agent():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("extract_preferences", extract_preferences)
    workflow.add_node("find_destinations", find_destinations)
    workflow.add_node("create_itinerary", create_itinerary)
    workflow.add_node("handle_followup", handle_followup)

    # Add edges
    workflow.add_edge("extract_preferences", "find_destinations")
    workflow.add_edge("find_destinations", "create_itinerary")
    workflow.add_conditional_edges("create_itinerary", lambda state: "handle_followup" if state.is_followup else END)
    workflow.add_edge("handle_followup", END)

    # Set entry point
    workflow.set_entry_point("extract_preferences")

    return workflow.compile()


travel_planner_graph = build_travel_agent()
