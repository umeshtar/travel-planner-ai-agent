from agent.state import AgentState


def handle_node_errors(func):
    def helper(state: AgentState):
        try:
            return func(state)
        except Exception as exc:
            print(f"{exc=}")
            state.history.append({'role': 'Something went wrong at our end, try again later'})
            state.print_itinerary = False
            return state

    return helper
