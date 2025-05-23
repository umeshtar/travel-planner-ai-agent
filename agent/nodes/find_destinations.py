import json
from pathlib import Path

from agent.state import AgentState
from agent.utils import handle_node_errors

DEFAULT_DESTINATION = {
    "name": "Rishikesh",
    "country": "India",
    "tags": [
        "beach",
        "culture"
    ],
    "budget_level": "high",
    "ideal_duration": [
        2,
        6
    ],
    "best_seasons": [
        "winter",
        "summer",
        "fall"
    ]
}


@handle_node_errors
def find_destinations(state: AgentState) -> AgentState:
    """
        Finds the top matching destinations for a given user based on preferences
        such as interests, budget level, and trip duration.

        Logic:
        - Loads all destinations from a JSON file.
        - Scores each destination based on:
            - Interest tag overlap
            - Budget level match
            - Ideal duration match
        - Selects the top 3 destinations with the highest scores.
        - Sets the best one as the selected destination.

        If no match is found, falls back to a default destination and
        adds a message in the history.
    """
    if not state.preferences:
        return state
    scored_destinations = []

    prefer_duration = state.preferences.get('duration', 0)
    prefer_budget_level = state.preferences.get('budget_level', '')
    prefer_interests = state.preferences.get('interests', [])

    with open(Path(__file__).resolve().parent.parent.parent / 'data' / 'destinations.json', "r") as f:
        data = json.load(f)

    if not data:
        state.history.append({'role': 'agent', 'message': 'No match found, however I have an suggestion'})
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
        state.history.append({'role': 'agent', 'message': 'No match found, however I have an suggestion'})
        state.selected_destination = DEFAULT_DESTINATION
        return state

    scored_destinations.sort(key=lambda a: a[0], reverse=True)
    top_destinations = [d for _, d in scored_destinations[:3]]

    state.destinations = top_destinations
    state.selected_destination = top_destinations[0]
    return state
