from pprint import pprint

from agent.graph import travel_planner_graph
from agent.state import AgentState

initial_state = AgentState(
    history=[
        {
            'role': 'user',
            'message': 'I want a 3-day trip focused on adventure',
        }
    ]
)

final_state = travel_planner_graph.invoke(initial_state)
pprint(final_state)
