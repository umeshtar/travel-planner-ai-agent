from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.nodes.create_itinerary import create_itinerary
from agent.nodes.extract_preferences import extract_preferences
from agent.nodes.find_destinations import find_destinations
from agent.nodes.handle_followup import handle_followup
from agent.state import AgentState


def entry_router(state: AgentState) -> AgentState:
    """ Dummy node for making entry point conditional """
    return state


# Build graph
def build_travel_agent():
    try:
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("entry_router", entry_router)
        workflow.add_node("extract_preferences", extract_preferences)
        workflow.add_node("find_destinations", find_destinations)
        workflow.add_node("create_itinerary", create_itinerary)
        workflow.add_node("handle_followup", handle_followup)

        # Entry routing
        workflow.add_conditional_edges(
            "entry_router",
            lambda state: "handle_followup" if state.is_followup else "extract_preferences"
        )

        # Main planning flow
        workflow.add_edge("extract_preferences", "find_destinations")
        workflow.add_edge("find_destinations", "create_itinerary")

        # After itinerary: go to follow-up or end
        workflow.add_conditional_edges(
            "create_itinerary",
            lambda state: "handle_followup" if state.is_followup else END
        )

        # After follow-up: either rerun or end
        workflow.add_conditional_edges(
            "handle_followup",
            lambda state: "extract_preferences" if not state.is_followup else END
        )

        # Set entry point
        workflow.set_entry_point("entry_router")

        return workflow.compile()

        # Sample Provided
        # # Add nodes
        # workflow.add_node("extract_preferences", extract_preferences)
        # workflow.add_node("find_destinations", find_destinations)
        # workflow.add_node("create_itinerary", create_itinerary)
        # workflow.add_node("handle_followup", handle_followup)
        #
        # # Add edges
        # workflow.add_edge("extract_preferences", "find_destinations")
        # workflow.add_edge("find_destinations", "create_itinerary")
        # workflow.add_conditional_edges("create_itinerary", lambda state: "handle_followup" if state.is_followup else END)
        # workflow.add_edge("handle_followup", END)
        #
        # # Set entry point
        # workflow.set_entry_point("extract_preferences")
        #
        # return workflow.compile()
    except Exception as e:
        print()


travel_planner_graph = build_travel_agent()
