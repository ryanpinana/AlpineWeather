import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True
)

def get_cached_weather(city):
    
    key = f"weather:{city.lower()}"

    data = redis_client.get(key)

    if data:
        weather = json.loads(data)

        weather["source"] = "Redis"

        return weather

    return None

def get_cached_weather_by_coordinates(latitude, longitude):
    key = f"weather:{latitude}:{longitude}"

    data = redis_client.get(key)

    if data:
        weather = json.loads(data)

        weather["source"] = "Redis"

        return weather

    return None

def cache_weather(city, weather_data):
    key = f"weather:{city.lower()}"

    redis_client.setex(
        key,
        3600,
        json.dumps(weather_data)
    )

def cache_weather_by_coordinates(latitude, longitude, weather_data):
    key = f"weather:{latitude}:{longitude}"

    redis_client.setex(
        key,
        3600,
        json.dumps(weather_data)
    )