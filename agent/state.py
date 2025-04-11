# Define the state structure
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AgentState:
    preferences: Dict[str, Any] = field(default_factory=dict)
    destinations: List[Dict[str, Any]] = field(default_factory=list)
    selected_destination: Dict[str, Any] = field(default_factory=dict)
    itinerary: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)
    is_followup: Optional[bool] = False
    print_itinerary: Optional[bool] = True
    exit_chat: Optional[bool] = True


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
