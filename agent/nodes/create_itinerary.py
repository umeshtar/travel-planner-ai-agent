def create_itinerary(state):
    state.itinerary = {
        "destination": "Paris",
        "duration": 4,
        "days": [
            {"day": 1, "activities": ["Arrival in Paris", "Visit Eiffel Tower"]},
            {"day": 2, "activities": ["Louvre Museum", "French food tour"]},
            {"day": 3, "activities": ["Notre-Dame", "Walk along the Seine"]},
            {"day": 4, "activities": ["Relax at a cafe", "Pack up and depart"]}
        ]
    }
    return state
