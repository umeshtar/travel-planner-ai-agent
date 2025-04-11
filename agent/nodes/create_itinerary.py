import random
from agent.state import AgentState

RECUR_LIMIT_CHECK = 100

ACTIVITY_MAPPING = {
    "cold": [
        "Sip hot chocolate at a cozy cafe",
        "Take a winter walk in layered clothing",
        "Visit a local wool or handicraft market",
        "Enjoy a scenic mountain view with warm drinks"
    ],
    "culture": [
        "Visit a local museum",
        "Explore a historic fort or palace",
        "Attend a cultural dance or music show",
        "Walk through traditional markets"
    ],
    "food": [
        "Try popular local street food",
        "Have lunch at a traditional restaurant",
        "Visit a local tea or coffee house",
        "Join a food tasting tour"
    ],
    "adventure": [
        "Go trekking in the nearby hills",
        "Try river rafting or paragliding",
        "Zip-lining or rappelling session",
        "Explore off-road trails by jeep"
    ],
    "nature": [
        "Take a scenic nature walk",
        "Visit a botanical garden or forest trail",
        "Birdwatching in the early morning",
        "Relax by a natural lake or river"
    ],
    "spiritual": [
        "Morning visit to a temple or shrine",
        "Attend a local aarti or prayer ceremony",
        "Meditation session in a peaceful place",
        "Visit a spiritual learning center"
    ],
    "romantic": [
        "Sunset boat ride",
        "Dinner with a view",
        "Walk through a garden or lakeside",
        "Visit a scenic viewpoint"
    ],
    "relaxation": [
        "Enjoy spa or wellness therapy",
        "Take a leisure walk along the beach/lake",
        "Sip coffee with a view",
        "Read or journal in a peaceful cafe"
    ],
    "history": [
        "Visit a historical museum",
        "Explore ancient ruins",
        "Guided heritage tour",
        "Walk along historical streets"
    ],
    "architecture": [
        "Take a heritage architecture walk",
        "Visit famous buildings and monuments",
        "Photo tour of architectural highlights",
        "Study unique designs of local houses"
    ],
    "snow": [
        "Build a snowman",
        "Try snowboarding or skiing",
        "Snow trek with a guide",
        "Hot drink in a hillside cafe"
    ]
}

GENERAL_ACTIVITIES = [
    "Take a guided city tour to explore local highlights",
    "Enjoy a peaceful morning walk in a nearby park",
    "Have a slow breakfast at a recommended local cafe",
    "Visit a local bazaar or handicraft market",
    "Relax at a public square or scenic viewpoint",
    "Try a local dessert or beverage unique to the city",
    "Attend any live street performance or fair",
    "Take a short photography walk",
    "Spend time journaling or reading in a quiet cafe",
    "Chat with locals or your host to learn about the culture"
]


def create_itinerary(state: AgentState)-> AgentState:
    # if state.is_followup:
    #     return state

    preferences = state.preferences
    selected_destination = state.selected_destination
    if not selected_destination:
        return state

    destination = selected_destination.get('name')
    duration = preferences.get('duration')
    interests = preferences.get('interests')
    prefer_activity_map = {k: random.sample(v, min(len(v), 5)) for k, v in ACTIVITY_MAPPING.items() if k in interests}
    general_activities = GENERAL_ACTIVITIES.copy()

    days = []
    active_tag = None
    for day in range(1, duration + 1):
        activities = []

        if day == 1:
            activities.append(f'Arrival in {destination}')

        # recur_limit = RECUR_LIMIT_CHECK
        while True:
            # recur_limit -= 1
            # if recur_limit == 0:
            #     state.history.append({'role': 'agent', 'message': 'Something Went Wrong'})
            #     return state

            if len(activities) == 2 or (len(activities) == 1 and day == duration):
                break

            if not prefer_activity_map:
                general_activity = random.choice(general_activities)
                activities.append(general_activity)
                general_activities.remove(general_activity)
                continue

            if active_tag is None:
                active_tag = random.choice(list(prefer_activity_map.keys()))

            available_activities = prefer_activity_map.get(active_tag, [])
            if available_activities:
                activity = random.choice(available_activities)
                activities.append(activity)
                prefer_activity_map[active_tag].remove(activity)
            else:
                del prefer_activity_map[active_tag]
                active_tag = None

        if len(activities) == 1 and day == duration:
            activities.append(f'Pack up and depart')

        days.append(dict(day=day, activities=activities))

    state.itinerary = {
        'destination': destination,
        'duration': duration,
        'days': days
    }
    return state
