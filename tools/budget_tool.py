from langchain.tools import tool

@tool
def estimate_budget(data: dict) -> dict:
    """
    Estimate trip budget from structured inputs.
    Expected input:
    {
        "flight_price": int,
        "hotel_price_per_night": int,
        "days": int
    }
    """
    flight = data["flight_price"]
    hotel_per_night = data["hotel_price_per_night"]
    days = data["days"]

    hotel_cost = hotel_per_night * days
    food_transport = days * 1500
    total = flight + hotel_cost + food_transport

    return {
        "flight": flight,
        "hotel": hotel_cost,
        "food": food_transport,
        "total": total
    }
