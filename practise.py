import itertools
import random
from difflib import get_close_matches
from random import choice

print({'5'} or {'1'})
print({} or {'1'})

a, b = [5, 7]
print(a, b)

print(len({'a': 1, 'b': 2}))

for i in range(10):
    print(choice([11, 23, 32]))

a = [1, 2, 4]
b = a.copy()
b.remove(2)
print(a)
print(b)

interest_cycle = itertools.cycle(['a', 'b', 'c', 'd'])
tag = next(interest_cycle)
print(tag)
tag = next(interest_cycle)
print(tag)
tag = next(interest_cycle)
print(tag)

import random
import json

# Define tag pools
all_tags = [
    "adventure", "nature", "spiritual", "culture", "food", "romantic", "relaxation",
    "snow", "history", "architecture", "beach", "cold", "mountains", "road-trip",
]

budget_levels = ["low", "medium", "high"]
seasons = ["spring", "summer", "monsoon", "fall", "winter"]

# 80 Indian cities or travel destinations
indian_cities = [
    "Rishikesh", "Manali", "Leh", "Udaipur", "Jaipur", "Jaisalmer", "Shimla", "Kullu", "Amritsar", "Dharamshala",
    "Goa", "Mumbai", "Pune", "Lonavala", "Alibaug", "Nashik", "Mount Abu", "Kodaikanal", "Ooty", "Mysore",
    "Hampi", "Chikmagalur", "Coorg", "Gokarna", "Varkala", "Munnar", "Alleppey", "Thekkady", "Wayanad", "Kochi",
    "Hyderabad", "Warangal", "Bangalore", "Chennai", "Pondicherry", "Madurai", "Rameswaram", "Tirupati", "Vizag",
    "Kolkata", "Darjeeling", "Kalimpong", "Gangtok", "Shillong", "Kaziranga", "Majuli", "Agartala", "Itanagar",
    "Aizawl", "Imphal", "Patna", "Bodh Gaya", "Rajgir", "Nalanda", "Ranchi", "Deoghar", "Bhubaneswar", "Puri",
    "Konark", "Cuttack", "Jabalpur", "Khajuraho", "Indore", "Bhopal", "Gwalior", "Ujjain", "Nagpur", "Aurangabad",
    "Ajanta", "Ellora", "Varanasi", "Prayagraj", "Lucknow", "Ayodhya", "Mathura", "Vrindavan", "Agra", "Delhi"
]


# Generate destination entries
def generate_destinations(cities, count=80):
    destinations = []
    for name in cities[:count]:
        tags = random.sample(all_tags, k=random.randint(2, 4))
        budget = random.choice(budget_levels)
        duration = sorted(random.sample(range(2, 8), 2))
        best_season = random.sample(seasons, k=random.randint(1, 3))
        destination = {
            "name": name,
            "country": "India",
            "tags": tags,
            "budget_level": budget,
            "ideal_duration": duration,
            "best_seasons": best_season
        }
        destinations.append(destination)
    return destinations


# Generate
destinations_data = generate_destinations(indian_cities, 80)
from pathlib import Path

# Save to a JSON file
# output_path = Path("data/indian_destinations.json")
# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump(destinations_data, f, indent=2)

print(get_close_matches('not luxury', ['budget', 'luxury', 'cheap', 'expensive', 'not expensive'], n=1))
print(get_close_matches('weekend', 'plan    my weekend       trip     '.split(' '), n=1))
print(get_close_matches('luxury', 'I want a weeked naturl trip, at low budgt'.split(' '), n=1))
print(get_close_matches('expensive', 'I want a weeked naturl trip, at low budgt'.split(' '), n=1))
print(get_close_matches('save money', 'I want a weeked naturl trip, at money expensive'.split(' '), n=1))
