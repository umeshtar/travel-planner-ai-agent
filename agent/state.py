# Define the state structure
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AgentState:
    """
        Represents the full state of the Travel Planner AI Agent at any point
        during the conversation.

        Attributes:
            preferences (dict): Extracted user preferences such as duration, interests, and budget.
            destinations (list): Top matched destinations based on preferences.
            selected_destination (dict): The destination selected by the agent for planning.
            itinerary (dict): The full itinerary including destination, duration, and day-wise activities.
            history (list): A conversation history of user and agent messages.
            is_followup (bool): Flag to determine if the current input is a follow-up.
            print_itinerary (bool): Controls whether the itinerary should be printed in the CLI.
            terminate_program (bool): Controls whether the Chat ends on user conformation in the CLI.
    """
    preferences: Dict[str, Any] = field(default_factory=dict)
    destinations: List[Dict[str, Any]] = field(default_factory=list)
    selected_destination: Dict[str, Any] = field(default_factory=dict)
    itinerary: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)
    is_followup: Optional[bool] = False
    print_itinerary: Optional[bool] = True
    terminate_program: Optional[bool] = False

# Initial State
# AgentState(
#     preferences={},
#     destinations=[],
#     selected_destination={},
#     itinerary={},
#     history=[],
#     is_followup=False
# )

# Middle State
# AgentState(
#     preferences={
#         "duration": 4,
#         "budget_level": "medium",
#         "interests": ["culture", "food"]
#     },
#     destinations=[
#         {"name": "Paris", "tags": ["culture", "food", "romantic"]},
#         {"name": "Rome", "tags": ["history", "culture", "food"]}
#     ],
#     selected_destination={"name": "Paris", "tags": ["culture", "food", "romantic"]},
#     itinerary={},
#     history=[
#         {"role": "user", "message": "I want a 4-day trip focused on culture and food"}
#     ],
#     is_followup=False
# )

# Final State
# AgentState(
#     preferences={
#         "duration": 4,
#         "budget_level": "medium",
#         "interests": ["culture", "food"]
#     },
#     destinations=[
#         {"name": "Paris", "tags": ["culture", "food", "romantic"]},
#         {"name": "Rome", "tags": ["history", "culture", "food"]}
#     ],
#     selected_destination={"name": "Paris", "tags": ["culture", "food", "romantic"]},
#     itinerary={
#         "destination": "Paris",
#         "duration": 4,
#         "days": [
#             {"day": 1, "activities": ["Arrival in Paris", "Visit Eiffel Tower"]},
#             {"day": 2, "activities": ["Louvre Museum", "French food tour"]},
#             {"day": 3, "activities": ["Notre-Dame", "Walk along the Seine"]},
#             {"day": 4, "activities": ["Relax at a cafe", "Pack up and depart"]}
#         ]
#     },
#     history=[
#         {"role": "user", "message": "I want a 4-day trip focused on culture and food"},
#         {"role": "agent", "message": "How about Paris?"}
#     ],
#     is_followup=False
# )
