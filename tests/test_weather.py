import pytest
from app.services.weather_service import get_weather_data

def test_get_weather_data():
    # Test con una città nota
    weather = get_weather_data("Rome")
    assert weather.temperature is not None
    assert weather.windspeed is not None
    assert weather.weathercode is not None
    assert weather.humidity is not None
    assert weather.precipitation is not None