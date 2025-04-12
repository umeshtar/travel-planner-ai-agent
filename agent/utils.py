import re
import traceback
from copy import deepcopy
from difflib import get_close_matches

import requests

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
        except Exception as node_exc:
            print(traceback.format_exc())
            print(f"{node_exc=}")
            state = original_state
            state.history.append({'role': 'Something went wrong at our end, try again later'})
            state.print_itinerary = False
            return state

    return helper


def get_weather_forecast(city_name: str, days: int = 3) -> list[str]:
    """
    Fetch weather forecast using Open-Meteo API based on city name.
    Uses simple city -> lat/lon lookup and gets daily conditions.
    """
    try:
        # Step 1: Geocoding (city to lat/lon)
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_resp = requests.get(geo_url, params={"name": city_name, "count": 1})
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            return ["Unknown"] * days

        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]

        # Step 2: Get weather forecast
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "weathercode",
            "forecast_days": days,
            "timezone": "auto"
        }

        weather_resp = requests.get(weather_url, params=weather_params)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        # Map weather codes to human-readable terms
        code_map = {
            0: "Clear", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Foggy", 48: "Freezing Fog", 51: "Light Drizzle", 61: "Rain",
            71: "Snow", 95: "Thunderstorm"
        }

        codes = weather_data["daily"]["weathercode"][:days]
        return [code_map.get(code, "Unknown") for code in codes]

    except Exception as weather_api_exc:
        print(f"{weather_api_exc=}")
        return ["Weather unavailable"] * days
