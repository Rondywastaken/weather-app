import requests
from flask import *

weather_api = "https://api.open-meteo.com/v1/forecast"
geocoding_api = "https://geocoding-api.open-meteo.com/v1/search"

def get_coordinates(location: str) -> tuple[str, str, float, float]:
    res = requests.get(
        url=geocoding_api,
        params={"name": location, "count": 1} # default count is 10
    )

    data = res.json()

    # API sometimes does not return an error on obscure input
    # Additional check if a result is even returned
    if res.status_code == 400 or data.get("error") or not data.get("results"):
        raise ValueError(f"No results found for '{location}'")

    result = data["results"][0] # We only want the first city
    return (result["country"], result["name"], result["latitude"], result["longitude"])

def get_weather(location: str):
    country, city, lat, lon = get_coordinates(location)

    res = requests.get(
        url=weather_api,
        params={
            "models": "best_match",
            "latitude": lat,
            "longitude": lon,
            "timezone": "auto",
            "hourly": "temperature_2m",
        }
    )

    data = res.json()

    # Already checked if city exists inside get_coordinates()
    # Simply checking if this request fails
    if res.status_code == 400 or data.get("error"):
        raise ValueError(f"No results found for '{location}'")

    return data, country, city