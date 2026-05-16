import json
import os
from langchain.tools import tool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

@tool
def discover_places(city: str) -> list:
    """
    Discover top places to visit in a city.
    """
    city = city.replace("'", "").replace('"', "").strip().lower()

    with open("data/places.json", "r") as f:
        places = json.load(f)

    return [
        p["name"] for p in places
        if p["city"].lower() == city
    ][:5]