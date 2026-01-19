import requests

def get_weather(city: str, days: int = 3) -> dict:
    """
    Get weather forecast using Open-Meteo (no agent, no LangChain).
    """
    # --- Geocoding ---
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_res = requests.get(
        geo_url, params={"name": city, "count": 1}
    ).json()

    if "results" not in geo_res:
        return {"days": []}

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    # --- Weather Forecast ---
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_res = requests.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "weathercode,temperature_2m_max",
            "forecast_days": days,
            "timezone": "auto",
        },
    ).json()

    daily = weather_res["daily"]

    return {
        "days": [
            {
                "day": i + 1,
                "temp": daily["temperature_2m_max"][i],
                "code": daily["weathercode"][i],
            }
            for i in range(days)
        ]
    }
