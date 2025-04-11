import json
from pathlib import Path

from agent.state import AgentState
from agent.utils.handle_node_errors import handle_node_errors

DEFAULT_DESTINATION = {
    "name": "Rishikesh",
    "country": "India",
    "tags": ["adventure", "nature", "spiritual"],
    "budget_level": "low",
    "ideal_duration": [2, 5],
    "best_seasons": ["spring", "winter"]
}

NAMED_DESTINATIONS = []


@handle_node_errors
def find_destinations(state: AgentState)-> AgentState:
    scored_destinations = []

    prefer_duration = state.preferences.get('duration', 3)
    prefer_budget_level = state.preferences.get('budget_level', 'medium')
    prefer_interests = state.preferences.get('interests', ['culture'])

    with open(Path(__file__).resolve().parent.parent.parent / 'data' / 'destinations.json', "r") as f:
        data = json.load(f)

    if not data:
        state.history.append({'role': 'agent', 'message': 'No match found, however I have an option'})
        state.selected_destination = DEFAULT_DESTINATION
        return state

    for d in data:
        tags = d.get('tags', [])
        budget_level = d.get('budget_level', '')
        ideal_duration = d.get('ideal_duration', [])

        match_score = 0
        for tag in tags:
            if tag.lower() in prefer_interests:
                match_score += 1

        if prefer_budget_level == budget_level.lower():
            match_score += 1

        if len(ideal_duration) == 2:
            min_duration, max_duration = ideal_duration
            if min_duration <= prefer_duration <= max_duration:
                match_score += 1

        if match_score:
            scored_destinations.append((match_score, d))

    if not scored_destinations:
        state.history.append({'role': 'agent', 'message': 'No match found, however I have an option'})
        state.selected_destination = DEFAULT_DESTINATION
        return state

    scored_destinations.sort(key=lambda a: a[0], reverse=True)
    top_destinations = [d for _, d in scored_destinations[:3]]

    state.destinations = top_destinations
    state.selected_destination = top_destinations[0]
    return state
