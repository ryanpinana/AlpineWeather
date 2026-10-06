from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from services.weather_service import get_weather, search_cities, get_weather_by_coordinates

weather_bp = Blueprint(
    "weather",
    __name__
)

@weather_bp.route("/")
@login_required
def search():
    return render_template("search.html")

@weather_bp.route("/weather")
@login_required
def weather():

    city = request.args.get("city")

    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if latitude and longitude:

        weather_data = get_weather_by_coordinates(
            latitude,
            longitude,
            city_name=city
        )

    else:

        weather_data = get_weather(city)

    if weather_data is None:

        return render_template(
            "search.html",
            error="Città non trovata."
        )

    return render_template(
        "weather.html",
        weather=weather_data
    )

@weather_bp.route("/autocomplete")
@login_required
def autocomplete():

    query = request.args.get("q", "")

    if len(query) < 2:
        return jsonify([])

    cities = search_cities(query)

    return jsonify(cities)