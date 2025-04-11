from agent.state import AgentState


def handle_followup(state: AgentState)-> AgentState:
    if not state.preferences:
        return state

    state.preferences['duration'] = 2
    state.is_followup = False
    return state
