from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.nodes.create_itinerary import create_itinerary
from agent.nodes.extract_preferences import extract_preferences
from agent.nodes.find_destinations import find_destinations
from agent.nodes.handle_followup import handle_followup
from agent.state import AgentState


def entry_router(state: AgentState) -> AgentState:
    """
    Dummy entry node used to dynamically choose between a new flow
    or follow-up flow based on the current state's is_followup flag.
    """
    return state


# Build graph
def build_travel_agent():
    """
        Constructs and compiles the LangGraph-based workflow for the travel planner agent.

        Nodes:
            - entry_router: Selects entry path (new or follow-up).
            - extract_preferences: Extracts trip duration, interests, budget from user input.
            - find_destinations: Matches destinations based on preferences.
            - create_itinerary: Builds day-wise plan with activities.
            - handle_followup: Handles user changes and loops if needed.

        Flow:
            - New chat: entry_router → extract_preferences → find_destinations → create_itinerary → (followup or END)
            - Follow-up: entry_router → handle_followup → (extract_preferences or END)

        Returns:
            RunnableGraph: A compiled graph object ready to invoke.
    """
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


travel_planner_graph = build_travel_agent()
