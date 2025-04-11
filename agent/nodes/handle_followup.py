import random
import re
from difflib import get_close_matches

from agent.nodes.extract_preferences import INTEREST_TAGS, BUDGET_TAGS, BUDGET_LEVELS
from agent.state import AgentState
from agent.utils import handle_node_errors, spell_checker

SUCCESS_KWARGS = [
    "looks good",
    "sounds great",
    "looks great",
    "perfect",
    "good",
    "great",
    "like it",
    "thank",
    "done",
    "ok"
]
SHORT_TRIP_KWARGS = [
    "shorten",
    "shorter",
    "less days",
    "reduce days",
    "cut down",
    "make it shorter",
    "trim the trip",
    "too long",
    "decrease days"
]
EXTEND_TRIP_KWARGS = [
    "extend",
    "longer",
    "more days",
    "increase days",
    "add a day",
    "make it longer",
    "add more days",
    "long trip",
    "extra days"
]
SUCCESS_AND_UPDATE_MESSAGES = [
    "Glad you like it! Let's update your plan!",
    "Perfect! Updating the itinerary as per your changes.",
    "Thanks for the feedback! Adjusting things now.",
    "Awesome! Making those changes for you.",
    "Working on your updated trip now!",
    "Love that you're happy! We'll make the tweaks now.",
    "Let me fix that plan as requested.",
    "Glad it suits you! Adjusting it right away.",
    "Noted your changes – rebuilding the itinerary.",
    "Updating everything based on your feedback!"
]
SUCCESS_ONLY_MESSAGES = [
    "Glad you like it! Have a great trip!",
    "Awesome! Wishing you a memorable journey!",
    "Perfect! Hope your trip turns out amazing!",
    "Great! Everything looks set for your adventure!",
    "Cheers! You’re all set to explore.",
    "That’s wonderful! Enjoy every moment!",
    "All done – safe travels!",
    "Excellent! Your plan is locked in.",
    "Thanks! The itinerary is ready for your trip.",
    "Enjoy your journey – all the best!"
]
UPDATE_ONLY_MESSAGES = [
    "Sure! Let me update your plan now.",
    "Absolutely – making the changes now.",
    "Working on your updated preferences.",
    "Okay! Updating the itinerary as requested.",
    "Got it! Let’s refine your trip.",
    "Of course! Adjusting your travel plan.",
    "Right away – applying your changes.",
    "Sure thing! Just a moment to rework the details.",
    "Alright! We’ll revise it for you.",
    "Yes! Modifying your trip as asked."
]
CLARIFY_MESSAGES = [
    "I didn’t quite get that – could you clarify?",
    "Hmm, I’m not sure what you mean. Can you rephrase?",
    "Can you explain that a bit more?",
    "I couldn’t interpret that properly. Could you restate?",
    "Let me know what you'd like to change!",
    "Sorry, I’m confused – want to try again?",
    "Could you tell me more clearly what to update?",
    "I’m not sure I followed. Want to rephrase that?",
    "Not sure how to proceed – can you explain?",
    "Help me understand what you'd like to adjust."
]


@handle_node_errors
def handle_followup(state: AgentState) -> AgentState:
    """
        Handles user follow-up messages to modify their existing travel plan.

        This function parses the user's feedback and updates preferences such as:
        - Duration changes (e.g., "make it shorter", "add more days")
        - Interests (e.g., "add adventure", "include beach")
        - Budget updates (e.g., "tight budget", "more affordable")

        It also detects if the user has confirmed satisfaction with the plan
        and sets flags to either reprocess or end the conversation.

        Decision Outcomes:
        - ✅ `is_update=True` → Preferences updated, run graph again.
        - ✅ `is_success=True` → User liked the current plan (with or without updates).
        - ❌ Otherwise → Asks for clarification.
    """

    if not state.preferences:
        return state

    is_update = False
    is_success = False

    msg = ''
    if state.history:
        for h in state.history[::-1]:
            if h.get('role', '') == 'user':
                msg = h.get('message', '').lower().strip()
                break

    msg = spell_checker(msg, INTEREST_TAGS)
    msg = spell_checker(msg, BUDGET_TAGS)
    msg_lst = msg.split(' ')

    duration = state.preferences.get('duration', 3)
    match_duration = re.search(r"(\d+)\s*-?\s*(day|days)", msg)
    if match_duration:
        state.preferences["duration"] = int(match_duration.group(1))
        is_update = True
    elif get_close_matches('weekend', msg_lst, n=1):
        state.preferences["duration"] = 2
        is_update = True
    elif get_close_matches('week', msg_lst, n=1):
        state.preferences["duration"] = 7
        is_update = True
    elif any(kw in msg for kw in SHORT_TRIP_KWARGS):
        state.preferences["duration"] = duration - 1
        is_update = True
    elif any(kw in msg for kw in EXTEND_TRIP_KWARGS):
        state.preferences["duration"] = duration + 1
        is_update = True

    interests = state.preferences.get('interests', [])
    for tag in INTEREST_TAGS:
        if tag in msg and tag not in interests:
            state.preferences["interests"].append(tag)
            is_update = True

    for k in BUDGET_LEVELS:
        if k in msg:
            state.preferences['budget_level'] = BUDGET_LEVELS[k]
            is_update = True
            break

    if any(kw in msg for kw in SUCCESS_KWARGS):
        is_success = True

    if is_success and is_update:
        state.history.append({'role': 'agent', 'message': random.choice(SUCCESS_AND_UPDATE_MESSAGES)})
        state.is_followup = False
        state.print_itinerary = True
    elif is_success:
        state.history.append({'role': 'agent', 'message': random.choice(SUCCESS_ONLY_MESSAGES)})
        state.is_followup = True
        state.print_itinerary = False
    elif is_update:
        state.history.append({'role': 'agent', 'message': random.choice(UPDATE_ONLY_MESSAGES)})
        state.is_followup = False
        state.print_itinerary = True
    else:
        state.history.append({'role': 'agent', 'message': random.choice(CLARIFY_MESSAGES)})
        state.is_followup = True
        state.print_itinerary = False

    return state
