from agent.state import AgentState


def extract_preferences(state: AgentState):
    print(f"{state=}")
    if state.history:
        msg = state.history[-1].get('message', '')
        if msg:
            pass
    state.preferences = {
        "duration": 4,
        "budget_level": "medium",
        "interests": ["culture", "food"]
    }
    return state
