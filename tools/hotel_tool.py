import json
import os
from langchain.tools import tool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

@tool
def recommend_hotel(city: str) -> dict:
    """
    Recommend the best hotel in a city.
    """
    city = city.replace("'", "").replace('"', "").strip().lower()

    with open("data/hotels.json", "r") as f:
        hotels = json.load(f)

    city_hotels = [h for h in hotels if h["city"].lower() == city]
    best = max(city_hotels, key=lambda x: x["stars"])

    return {
        "name": best["name"],
        "stars": best["stars"],
        "price_per_night": best["price_per_night"]
    }
