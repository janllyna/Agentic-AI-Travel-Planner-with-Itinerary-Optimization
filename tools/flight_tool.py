import json
import os
import re
from langchain.tools import tool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

@tool
def search_flights(route: str) -> dict:
    """
    Find the cheapest flight between two cities.
    Accepts formats like:
    - Hyderabad to Goa
    - Hyderabad-Goa
    - Hyderabad – Goa
    - hyderabad goa
    """
    
    route = route.lower().replace("'", "").replace('"', "").strip()

    
    route = re.sub(r"\s*[-–]\s*", " to ", route)
    route = re.sub(r"\s+", " ", route)

    if " to " not in route:
        raise ValueError("Invalid route format. Use: Hyderabad to Goa")

    source, destination = [x.strip().title() for x in route.split(" to ", 1)]

    
    with open(os.path.join(DATA_DIR, "flights.json"), "r", encoding="utf-8") as f:
        flights = json.load(f)

    matches = [
        f for f in flights
        if f["from"].lower() == source.lower()
        and f["to"].lower() == destination.lower()
    ]

    if not matches:
        raise ValueError(f"No flights found from {source} to {destination}")

    flight = min(matches, key=lambda x: x["price"])

    return {
        "airline": flight["airline"],
        "price": flight["price"],
        "departure": flight["departure_time"],
        "from": flight["from"],
        "to": flight["to"]
    }
