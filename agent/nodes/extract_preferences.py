import re
from difflib import get_close_matches

from agent.state import AgentState

from agent.utils import spell_checker, handle_node_errors

SEASONAL_TAGS = {
    "winter": [
        "snow", "cold", "spiritual", "romantic", "relaxation", "culture", "history", "nature", "mountains"
    ],
    "summer": [
        "beach", "adventure", "road-trip", "nature", "mountains", "food", "culture", "relaxation"
    ],
    "monsoon": [
        "spiritual", "nature", "cold", "romantic", "architecture"
    ],
    "spring": [
        "nature", "romantic", "culture", "architecture", "relaxation", "adventure"
    ],
    "fall": [
        "nature", "culture", "history", "architecture", "romantic", "spiritual"
    ]
}
INTEREST_TAGS = {
    "beach",
    "culture",
    "food",
    "adventure",
    "architecture",
    "nature",
    "spiritual",
    "relaxation",
    "snow",
    "cold",
    "road-trip",
    "romantic",
    "winter",
    "summer",
    "monsoon",
    "history",
    "mountains",
}
BUDGET_LEVELS = {
    # ➤ Negations and specific phrases first (to avoid false matches)
    "not too expensive": "medium",
    "not too cheap": "medium",
    "no budget limit": "high",
    "i can spend freely": "high",
    "don't care about money": "high",
    "as cheap as possible": "low",
    "not much to spend": "low",
    "on a shoestring": "low",

    # ➤ Low Budget
    "cheap": "low",
    "low budget": "low",
    "limited budget": "low",
    "tight budget": "low",
    "budget friendly": "low",
    "affordable": "low",
    "inexpensive": "low",
    "economical": "low",
    "backpacking": "low",
    "money saving": "low",

    # ➤ High Budget (put last)
    "luxury": "high",
    "luxurious": "high",
    "expensive": "high",
    "high budget": "high",
    "upper budget": "high",
    "premium": "high",
    "high-end": "high",
    "costly": "high",

    # ➤ Medium Budget (mid-level tones)
    "medium budget": "medium",
    "average budget": "medium",
    "moderate": "medium",
    "balanced": "medium",
    "mid-range": "medium",
    "reasonable": "medium",
    "okay budget": "medium",
    "mid-level": "medium",
}
BUDGET_TAGS = [
    'budget',
    'expensive',
    'cheap',
    'limited',
    'affordable',
    'inexpensive',
    'economical',
    'luxury',
    'luxurious',
    'premium',
    'costly',
    'moderate',
    'balanced',
    'reasonable',
]


@handle_node_errors
def extract_preferences(state: AgentState) -> AgentState:
    """
        Extracts user travel preferences such as duration, budget level, and interests
        from the most recent message in the conversation history. This is the entry point
        for parsing a new user's input.

        Flow:
            - Uses regex to detect number of days or keywords like 'weekend'.
            - Applies fuzzy matching to infer budget and interests.
            - Uses a spell checker to fix input typos before parsing.
    """
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

    msg = spell_checker(msg, INTEREST_TAGS)
    msg = spell_checker(msg, BUDGET_TAGS)
    msg_lst = msg.split(' ')

    # Fetch duration
    match_duration = re.search(r"(\d+)\s*-?\s*(day|days)", msg)
    if match_duration:
        duration = int(match_duration.group(1))
    elif get_close_matches('weekend', msg_lst, n=1):
        duration = 2
    elif get_close_matches('week', msg_lst, n=1):
        duration = 7

    # Fetch budget
    for k in BUDGET_LEVELS:
        if k in msg:
            budget_level = BUDGET_LEVELS[k]
            break

    # Fetch interests
    interests = {i for i in INTEREST_TAGS if get_close_matches(i, msg_lst, n=1)} or interests

    # Update State
    state.preferences = {
        "duration": duration,
        "budget_level": budget_level,
        "interests": list(interests)
    }
    return state
