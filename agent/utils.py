import re
import traceback
from copy import deepcopy
from difflib import get_close_matches
from pathlib import Path

from agent.state import AgentState


def spell_checker(msg, valid_words):
    words = re.findall(r'\w+', msg)
    corrected = []
    for word in words:
        if word in valid_words:
            corrected.append(word)
        else:
            match = get_close_matches(word, valid_words, n=1)
            corrected.append(match[0] if match else word)
    return ' '.join(corrected)


def handle_node_errors(func):
    def helper(state: AgentState):
        original_state = deepcopy(state)
        try:
            return func(state)
        except Exception as exc:
            print(traceback.format_exc())
            print(f"{exc=}")
            state = original_state
            state.history.append({'role': 'Something went wrong at our end, try again later'})
            state.print_itinerary = False
            return state

    return helper
