from flask import Blueprint, render_template, request
from flask_login import login_required
from services.weather_service import get_weather

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

    if not city:
        return render_template(
            "search.html",
            error="Inserisci una città"
        )

    weather_data = get_weather(city)

    if weather_data is None:
        return render_template(
            "search.html",
            error="Città non trovata"
        )

    return render_template(
        "weather.html",
        weather=weather_data
    )