from pprint import pprint

from agent.graph import travel_planner_graph
from agent.state import AgentState


def print_itinerary(itinerary: dict):
    """ Pretty prints a day-wise travel itinerary to the console. """
    print(f"\n🧳 Your {itinerary['duration']}-day itinerary for {itinerary['destination']}:\n")
    for day in itinerary['days']:
        print(f"Day {day['day']}:")
        for act in day['activities']:
            print(f"  - {act}")
    print()


# Start fresh conversation
state = AgentState()

print("✈️ Travel Planner AI Agent")
print("Type 'exit' to quit.\n")

# Initial input
user_input = input("🧍 You: ").strip()

while user_input.lower() not in {"exit", "quit"}:
    # Add user message to history
    state.history.append({"role": "user", "message": user_input})
    state.is_followup = bool(state.preferences)  # If preferences exist, it's follow-up

    # Run graph
    result = travel_planner_graph.invoke(state)

    # Convert back to AgentState
    state = AgentState(**result)

    # Print agent's last response (from history)
    for h in state.history[::-1]:
        if h.get("role") == "agent":
            print(f"\n🤖 Agent: {h['message']}")
            break

    # Print updated itinerary if available
    if state.itinerary and state.print_itinerary:
        print_itinerary(state.itinerary)

    # Get follow-up input
    user_input = input("🧍 You: ").strip()

print("\n👋 Goodbye! Safe travels!\n")

# Initial Code for development
# initial_state = AgentState(
#     history=[
#         {
#             'role': 'user',
#             'message': 'I want to go for a vacation for 4 to 5 days, I like snow and cold environments.',
#         }
#     ]
# )
#
# follow_up  = travel_planner_graph.invoke(initial_state)
# pprint(follow_up)
# follow_up_state = AgentState(**follow_up)
#
# follow_up_state.history.append({'role': 'user', 'message': 'make it shorter'})
# follow_up_state.is_followup = True
#
# final_state = travel_planner_graph.invoke(follow_up_state)
# pprint(final_state)
