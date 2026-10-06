import requests
from services.redis_service import get_cached_weather, cache_weather


def get_city_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "it",
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    result = data["results"][0]

    return {
        "name": result["name"],
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


def get_weather(city):

    cached = get_cached_weather(city)

    if cached:
        print("DATI PRESI DA REDIS")

        return cached

    print("DATI PRESI DA OPEN-METEO")

    location = get_city_coordinates(city)

    if location is None:
        return None

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    weather_description = get_weather_description(
        current["weather_code"]
    )

    weather_data = {
        "city": location["name"],
        "country": location["country"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "apparent_temperature": current["apparent_temperature"],
        "wind_speed": current["wind_speed_10m"],
        "weather_description": weather_description
    }

    cache_weather(city, weather_data)

    weather_data["source"] = "Open-Meteo"

    return weather_data

def get_weather_description(code):
    descriptions = {
        0: "☀️ Sereno",

        1: "🌤️ Prevalentemente sereno",
        2: "⛅ Parzialmente nuvoloso",
        3: "☁️ Coperto",

        45: "🌫️ Nebbia",
        48: "🌫️ Nebbia con brina",

        51: "🌦️ Pioviggine leggera",
        53: "🌦️ Pioviggine moderata",
        55: "🌦️ Pioviggine intensa",

        61: "🌧️ Pioggia debole",
        63: "🌧️ Pioggia moderata",
        65: "🌧️ Pioggia intensa",

        71: "❄️ Neve debole",
        73: "❄️ Neve moderata",
        75: "❄️ Neve intensa",

        80: "🌦️ Rovesci leggeri",
        81: "🌦️ Rovesci moderati",
        82: "🌦️ Rovesci intensi",

        95: "⛈️ Temporale",
        96: "⛈️ Temporale con grandine",
        99: "⛈️ Temporale forte con grandine"
    }

    return descriptions.get(
        code,
        "Condizione sconosciuta"
    )