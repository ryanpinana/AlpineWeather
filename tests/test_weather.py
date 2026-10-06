from unittest.mock import patch


@patch("services.weather_service.get_weather")
def test_weather_search(
        mock_weather,
        logged_client):

    mock_weather.return_value = {
        "city": "Milano",
        "country": "Italia",
        "temperature": 25,
        "humidity": 60,
        "apparent_temperature": 26,
        "wind_speed": 10,
        "weather_description": "Sereno",
        "source": "Test"
    }

    response = logged_client.get(
        "/weather?city=Milano"
    )

    assert response.status_code == 200