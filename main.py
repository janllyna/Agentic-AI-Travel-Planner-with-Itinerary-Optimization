from agent import agent_executor
from tools.weather_tool import get_weather
from tools.places_tool import discover_places

import re


# -----------------------------
# Extract trip days
# -----------------------------
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
# Run agent
# -----------------------------
result = agent_executor.invoke({"input": query})

steps = result.get("intermediate_steps", [])


# -----------------------------
# Extract outputs safely
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


# -----------------------------
# Safety fallback values
# -----------------------------
if flight is None:
    print("No flight found.")
    exit()

if hotel is None:
    print("No hotel found.")
    exit()


destination = flight["to"]


# -----------------------------
# Force places if agent skipped
# -----------------------------
if places is None:
    places = discover_places.invoke(destination)


# -----------------------------
# Safety handling for places
# -----------------------------
if places is None:
    places = []

elif isinstance(places, list):
    pass

elif isinstance(places, str):

    cleaned = (
        places
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )

    places = [
        p.strip()
        for p in cleaned.split(",")
        if p.strip()
    ]

elif isinstance(places, dict):
    places = list(places.values())

else:
    places = [str(places)]


# -----------------------------
# Weather
# -----------------------------
days = extract_days(query)

weather_response = get_weather(destination, days)

weather_data = weather_response.get("days", [])


# -----------------------------
# Budget
# -----------------------------
flight_cost = flight["price"]

hotel_cost = hotel["price_per_night"] * days

food_cost = days * 1500

total_cost = (
    flight_cost +
    hotel_cost +
    food_cost
)


# -----------------------------
# FINAL OUTPUT
# -----------------------------
print(f"\nYour {days}-Day Trip to {destination}\n")


# -----------------------------
# Flight
# -----------------------------
print("Flight Selected:")

print(
    f"- {flight['airline']} "
    f"(₹{flight_cost}) – "
    f"Departs {flight['from']}\n"
)


# -----------------------------
# Hotel
# -----------------------------
print("Hotel Booked:")

print(
    f"- {hotel['name']} "
    f"(₹{hotel['price_per_night']}/night, "
    f"{hotel['stars']}-star)\n"
)


# -----------------------------
# Weather
# -----------------------------
print("Weather:")

if weather_data:

    for d in weather_data:

        print(
            f"- Day {d['day']}: "
            f"{decode_weather(d['code'])} "
            f"({d['temp']}°C)"
        )

else:
    print("- Weather data unavailable")

print()


# -----------------------------
# Itinerary
# -----------------------------
print("Itinerary:")

if places:

    for day in range(days):

        place = places[day % len(places)]

        print(f"Day {day + 1}: {place}")

else:
    print("No places available.")

print()


# -----------------------------
# Budget
# -----------------------------
print("Estimated Total Budget:")

print(f"- Flight: ₹{flight_cost}")

print(f"- Hotel: ₹{hotel_cost}")

print(f"- Food & Travel: ₹{food_cost}")

print("-------------------------------------")

print(f"Total Cost: ₹{total_cost}")