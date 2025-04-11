import re
import traceback
from copy import deepcopy
from difflib import get_close_matches

from agent.state import AgentState


def spell_checker(msg, valid_words):
    """
        Attempts to correct potential typos in a user's message by comparing
        each word against a set of valid vocabulary terms.

        Args:
            msg (str): The raw input message from the user.
            valid_words (list | set): A list of accepted valid keywords (e.g., interests, budget terms).

        Returns:
            str: The corrected message string where close matches are substituted.
    """
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
    """
        Decorator for safe execution of a node function. It captures exceptions,
        resets the state to its original form, and adds an error message to history.
    """

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
