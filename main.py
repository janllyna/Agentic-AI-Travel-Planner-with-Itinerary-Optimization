from agent import agent_executor
from tools.weather_tool import get_weather

import re

def extract_days(text: str, default=3) -> int:
    match = re.search(r"(\d+)\s*day", text.lower())
    if match:
        return int(match.group(1))
    return default

# -----------------------------
# Decode weather codes
# -----------------------------
def decode_weather(code):
    return {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        61: "Light Rain",
        63: "Moderate Rain",
        80: "Rain Showers"
    }.get(code, "Unknown")

# -----------------------------
# User input
# -----------------------------
query = input("Enter your trip request: ")

# -----------------------------
# Run agent (ONLY reasoning tasks)
# -----------------------------
result = agent_executor.invoke({"input": query})
steps = result["intermediate_steps"]

# -----------------------------
# Extract outputs SAFELY
# -----------------------------
flight = None
hotel = None
places = None

for action, output in steps:
    tool_name = action.tool

    if tool_name == "search_flights" and flight is None:
        flight = output

    elif tool_name == "recommend_hotel" and hotel is None:
        hotel = output

    elif tool_name == "discover_places" and places is None:
        places = output



if not isinstance(places, list):
    places = list(places)


destination = flight["to"]

# -----------------------------
# Weather (manual, deterministic)
# -----------------------------
days = extract_days(query)
weather_data = get_weather(destination, days)["days"]

# -----------------------------
# Budget (manual, deterministic)
# -----------------------------
flight_cost = flight["price"]
hotel_cost = hotel["price_per_night"] * days
food_cost = days * 1500
total_cost = flight_cost + hotel_cost + food_cost

# -----------------------------
# FINAL OUTPUT
# -----------------------------
print(f"\nYour {days}-Day Trip to {destination}\n")

print("Flight Selected:")
print(f"- {flight['airline']} (₹{flight_cost}) – Departs {flight['from']}\n")

print("Hotel Booked:")
print(f"- {hotel['name']} (₹{hotel['price_per_night']}/night, {hotel['stars']}-star)\n")

print("Weather:")
for d in weather_data:
    print(f"- Day {d['day']}: {decode_weather(d['code'])} ({d['temp']}°C)")
print()

print("Itinerary:")


if not isinstance(places, list):
    places = list(places)

places_per_day = max(1, len(places) // days)

for day in range(days):
    start = day * places_per_day
    end = start + places_per_day
    day_places = places[start:end]

    if day_places:
        print(f"Day {day + 1}: {', '.join(day_places)}")

print()


print("Estimated Total Budget:")
print(f"- Flight: ₹{flight_cost}")
print(f"- Hotel: ₹{hotel_cost}")
print(f"- Food & Travel: ₹{food_cost}")
print("-------------------------------------")
print(f"Total Cost: ₹{total_cost}")
