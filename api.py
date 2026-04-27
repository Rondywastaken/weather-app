import requests
from datetime import datetime

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
            "hourly": ["temperature_2m", "weather_code"],
            "daily": ["temperature_2m_mean", "weather_code"]
        }
    )

    data = res.json()

    # Already checked if city exists inside get_coordinates()
    # Simply checking if this request fails
    if res.status_code == 400 or data.get("error"):
        raise ValueError(f"No results found for '{location}'")

    return data, country, city

def get_current_hour_index(data: dict) -> int:
    times = data["hourly"]["time"]
    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")
    return times.index(current_time)

def get_weather_icon(code: int) -> str:
    # following the WMO standard as given by API
    if code == 0: 
        return "☀️"   
    elif code in [1, 2, 3]: 
        return "⛅"
    elif code in [45, 48]: 
        return "🌫️"
    elif code in [51, 53, 55, 56, 57]: 
        return "🌦️" 
    elif code in [61, 63, 65, 66, 67, 80, 81, 82]: 
        return "🌧️"
    elif code in [71, 73, 75, 77, 85, 86]: 
        return "❄️"
    elif code in [95, 96, 99]: 
        return "⛈️"
    else: 
        return "" 

def get_hours_by_day(times: list[str], temperatures: list[float]) -> dict:
    hours_by_day = {}
    for i, time in enumerate(times):
        date, hour = time.split("T")
        hours_by_day.setdefault(date, {"hours": [], "temps": []})
        hours_by_day[date]["hours"].append(hour)
        hours_by_day[date]["temps"].append(temperatures[i])
    return hours_by_day
