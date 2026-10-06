import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
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

def cache_weather(city, weather_data):
    key = f"weather:{city.lower()}"

    redis_client.setex(
        key,
        3600,
        json.dumps(weather_data)
    )