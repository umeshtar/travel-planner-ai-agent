import re

from agent.state import AgentState
from agent.utils.handle_node_errors import handle_node_errors

SEASONAL_TAGS = {
    'winter': ['nature'],
    'summer': ['beach', 'snow', 'mountains'],
    'monsoon': [''],
    'spring': ['nature'],
}
INTEREST_TAGS = {"culture", "food", "adventure", "nature", "spiritual", "relaxation", "cold", "winter", "summer", "monsoon"}
BUDGET_LEVELS = {
    'luxury': 'high',
    'expensive': 'high',
    'cheap': 'low',
    'high budget': 'high',
    'medium budget': 'medium',
    'medium cost': 'medium',
    'average budget': 'medium',
    'average cost': 'medium',
    'low budget': 'low',
    'budget': 'low',
}


@handle_node_errors
def extract_preferences(state: AgentState)-> AgentState:
    if state.preferences:
        return state

    # Initialize defaults for fallback
    msg = ''
    duration = 3
    budget_level = 'medium'
    interests = {'culture'}

    # Get message
    if state.history:
        # Get Latest User Message (Luckily Last One)
        for h in state.history[::-1]:
            if h.get('role', '') == 'user':
                msg = h.get('message', '').lower().strip()
                break

    # Fetch duration
    match_duration = re.search(r"(\d+)\s*-?\s*(day|days)", msg)
    if match_duration:
        duration = int(match_duration.group(1))
    elif 'weekend' in msg:
        duration = 2
    elif 'week' in msg:
        duration = 7

    # Fetch budget
    for k in BUDGET_LEVELS:
        if k in msg:
            budget_level = BUDGET_LEVELS[k]
            break

    # Fetch interests
    interests = {i for i in INTEREST_TAGS if i in msg} or interests

    # Update State
    state.preferences = {
        "duration": duration,
        "budget_level": budget_level,
        "interests": list(interests)
    }
    return state

