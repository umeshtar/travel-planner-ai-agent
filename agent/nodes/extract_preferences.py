import re

from agent.state import AgentState

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


def extract_preferences(state: AgentState):
    # print(f"{state=}")

    # Initialize defaults for fallback
    msg = ''
    duration = 3
    budget_level = 'medium'
    interests = {'culture'}
    if state.history:
        # Get Latest User Message (Luckily Last One)
        for h in state.history[::-1]:
            if h.get('role', '') == 'user':
                msg = h.get('message', '').lower()
                break

    # Fetch duration
    match_duration = re.search(r"(\d+)\s*-?\s*(day|days)", msg)
    if match_duration:
        duration = int(match_duration.group(1))
    elif 'week' in msg:
        duration = 7

    # Fetch budget
    for k in BUDGET_LEVELS:
        if k in msg:
            budget_level = BUDGET_LEVELS[k]
            break

    # Fetch interests
    interests = {i for i in INTEREST_TAGS if i in msg} or interests

    state.preferences = {
        "duration": duration,
        "budget_level": budget_level,
        "interests": list(interests)
    }
    return state


# Helper Functions
def get_user_prompt(history):
    if not history:
        return ''

    # Get Latest User Message (Luckily Last One)
    for h in history[::-1]:
        if h.get('role', '') == 'user':
            return h.get('message', '').lower()
    return ''
