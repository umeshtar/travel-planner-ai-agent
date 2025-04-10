from pprint import pprint

from agent.graph import travel_planner_graph
from agent.state import AgentState

initial_state = AgentState(
    history=[
        {
            'role': 'user',
            'message': 'I want to go for a vacation for 4 to 5 days, I like snow and cold environments.',
        }
    ]
)

final_state = travel_planner_graph.invoke(initial_state)
pprint(final_state)
