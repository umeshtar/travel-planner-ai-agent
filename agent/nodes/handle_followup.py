import re

from agent.nodes.extract_preferences import INTEREST_TAGS
from agent.state import AgentState
from agent.utils.handle_node_errors import handle_node_errors

SUCCESS_KWARGS = ["looks good", "sounds great", "looks great", "perfect", "good", "great", "like it", "thank", "done", "ok"]
SHORT_TRIP_KWARGS = ["shorten ", "shorter", "less day", "reduce day", "cut down"]


@handle_node_errors
def handle_followup(state: AgentState) -> AgentState:
    if not state.preferences:
        return state

    is_update = False
    is_success = False

    # Get message
    msg = ''
    if state.history:
        for h in state.history[::-1]:
            if h.get('role', '') == 'user':
                msg = h.get('message', '').lower().strip()
                break

    # Reduce Duration
    # Fetch updated duration
    duration = state.preferences.get('duration', 3)
    match_duration = re.search(r"(\d+)\s*-?\s*(day|days)", msg)
    if match_duration:
        state.preferences["duration"] = int(match_duration.group(1))
        is_update = True
    elif 'week' in msg:
        state.preferences["duration"] = 7
        is_update = True
    elif any(kw in msg for kw in ["shorter", "less days", "reduce trip", "cut down"]):
        state.preferences["duration"] = max(1, duration - 1)
        is_update = True
    elif any(kw in msg for kw in ["longer", "extend", "more days"]):
        state.preferences["duration"] = duration + 1
        is_update = True

    interests = state.preferences.get('interests', [])
    for tag in INTEREST_TAGS:
        if tag in msg and tag not in interests:
            state.preferences["interests"].append(tag)
            is_update = True

    if any(kw in msg for kw in SUCCESS_KWARGS):
        is_success = True

    if is_success and is_update:
        state.history.append({'role': 'agent', 'message': 'Glad you like it! lets work on your changes!'})
        state.is_followup = False
        state.print_itinerary = True
    elif is_success:
        state.history.append({'role': 'agent', 'message': 'Glad you like it! Have a great trip!'})
        state.is_followup = True
        state.print_itinerary = False
    elif is_update:
        state.history.append({'role': 'agent', 'message': "Sure! lets work on your changes!"})
        state.is_followup = False
        state.print_itinerary = True
    else:
        state.history.append({'role': 'agent', 'message': "I didn't understand that! Can you more clarify"})
        state.is_followup = True
        state.print_itinerary = False

    return state
