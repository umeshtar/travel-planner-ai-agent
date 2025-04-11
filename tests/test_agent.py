"""
tests.py

Unit tests for the core node functions of the Travel Planner AI Agent.

Covers:
- Preference extraction from user prompts.
- Destination matching based on preferences.
- Day-wise itinerary generation.
- Follow-up handling for user changes or confirmations.
"""

from agent.nodes.create_itinerary import create_itinerary
from agent.nodes.extract_preferences import extract_preferences
from agent.nodes.find_destinations import find_destinations
from agent.nodes.handle_followup import handle_followup
from agent.state import AgentState


def test_extract_preferences():
    """
        Test the extract_preferences node:
        - Validates duration, budget level, and interest extraction from realistic user prompts.
        - Checks for fuzzy spell correction and weekend/week keyword interpretation.
    """
    state = AgentState(
        history=[{"role": "user", "message": "I want a 5-day spiritual trip, not too expensive"}]
    )
    updated = extract_preferences(state)
    prefs = updated.preferences

    assert prefs["duration"] == 5
    assert prefs["budget_level"] in {"medium", "low"}
    assert "spiritual" in prefs["interests"]

    state = AgentState(
        history=[{"role": "user", "message": "I want a weeked naturl trip, at high budgt"}]
    )
    updated = extract_preferences(state)
    prefs = updated.preferences
    assert prefs["duration"] == 2
    assert prefs["budget_level"] in {"high"}
    assert "nature" in prefs["interests"]
    print("✅ test_extract_preferences passed")


def test_find_destinations():
    """
        Test the find_destinations node:
        - Ensures that the top match is selected based on preferences.
        - Validates the type and structure of the resulting destinations list.
    """
    state = AgentState(preferences={
        "duration": 4,
        "budget_level": "medium",
        "interests": ["culture", "nature"]
    })
    updated = find_destinations(state)
    assert updated.selected_destination
    assert isinstance(updated.destinations, list)
    assert updated.selected_destination
    assert isinstance(updated.selected_destination, dict)
    assert "name" in updated.selected_destination
    print("✅ test_find_destinations passed")


def test_create_itinerary():
    """
        Test the create_itinerary node:
        - Validates that an itinerary is generated for the given preferences and destination.
        - Ensures the correct number of days and destination name are included.
    """
    state = AgentState(
        preferences={
            "duration": 3,
            "interests": ["adventure", "food"]
        },
        selected_destination={"name": "Goa", "tags": ["beach", "food"]}
    )
    updated = create_itinerary(state)
    itinerary = updated.itinerary
    assert itinerary and itinerary["destination"] == "Goa"
    assert len(itinerary["days"]) == 3
    print("✅ test_create_itinerary passed")


def test_handle_followup_interest_addition():
    """
        Test follow-up handling when user wants to add an interest.
        - Checks if new interest is appended to preferences.
        - Ensures is_followup is correctly reset.
    """
    state = AgentState(
        preferences={"duration": 3, "interests": ["nature"]},
        history=[{"role": "user", "message": "Add some adventure too"}],
        is_followup=True
    )
    updated = handle_followup(state)
    assert "adventure" in updated.preferences["interests"]
    assert not updated.is_followup
    print("✅ test_handle_followup_interest_addition passed")


def test_handle_followup_duration_change():
    """
        Test follow-up handling when the user changes trip duration or is unclear.
        - Validates successful update of duration.
        - Also checks for fallback when no clear instructions are detected.
    """
    state = AgentState(
        preferences={"duration": 4, "interests": ["culture"]},
        history=[{"role": "user", "message": "Can we do 2 days instead?"}],
        is_followup=True
    )
    updated = handle_followup(state)
    assert updated.preferences["duration"] == 2
    assert not updated.is_followup

    state = AgentState(
        preferences={"duration": 3, "interests": ["nature"]},
        history=[{"role": "user", "message": "Hmm not sure"}],
        is_followup=True
    )
    updated = handle_followup(state)
    assert updated.is_followup
    assert "clarify" in updated.history[-1]["message"].lower()
    print("✅ test_handle_followup_duration_change passed")


if __name__ == "__main__":
    test_extract_preferences()
    test_find_destinations()
    test_create_itinerary()
    test_handle_followup_duration_change()
    test_handle_followup_interest_addition()
    print("\n🎉 All tests passed!")
