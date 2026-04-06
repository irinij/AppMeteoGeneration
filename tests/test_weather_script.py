import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Aggiungi il percorso del progetto per importare weather_script
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from weather_script import get_weather


@patch('weather_script.requests.get')
def test_get_weather_success(mock_get, capsys):
    """Test caso di successo con città valida."""
    # Mock per geocodifica
    mock_geo = MagicMock()
    mock_geo.status_code = 200
    mock_geo.json.return_value = [{"lat": "41.9028", "lon": "12.4964"}]

    # Mock per meteo
    mock_weather = MagicMock()
    mock_weather.status_code = 200
    mock_weather.json.return_value = {"current": {"temperature": 15.0, "windspeed": 10.0, "weathercode": 1, "relative_humidity_2m": 60.0, "precipitation": 0.0}}

    mock_get.side_effect = [mock_geo, mock_weather]

    get_weather("Rome")

    captured = capsys.readouterr()
    assert "Meteo attuale a Rome:" in captured.out
    assert "Temperatura: 15.0°C" in captured.out
    assert "Velocità del vento: 10.0 km/h" in captured.out
    assert "Umidità: 60.0%" in captured.out
    assert "Precipitazioni: 0.0 mm" in captured.out


@patch('weather_script.requests.get')
def test_get_weather_city_not_found(mock_get, capsys):
    """Test città non trovata."""
    mock_geo = MagicMock()
    mock_geo.status_code = 200
    mock_geo.json.return_value = []

    mock_get.return_value = mock_geo

    get_weather("CittàInesistente")

    captured = capsys.readouterr()
    assert "Errore: Città non trovata." in captured.out


@patch('weather_script.requests.get')
def test_get_weather_geocoding_error(mock_get, capsys):
    """Test errore API geocodifica."""
    from requests.exceptions import HTTPError

    mock_geo = MagicMock()
    mock_geo.status_code = 404
    mock_geo.raise_for_status.side_effect = HTTPError("404 Client Error")

    mock_get.return_value = mock_geo

    get_weather("Rome")

    captured = capsys.readouterr()
    assert "Errore di rete:" in captured.out


@patch('weather_script.requests.get')
def test_get_weather_weather_api_error(mock_get, capsys):
    """Test errore API meteo."""
    from requests.exceptions import HTTPError

    mock_geo = MagicMock()
    mock_geo.status_code = 200
    mock_geo.json.return_value = [{"lat": "41.9028", "lon": "12.4964"}]

    mock_weather = MagicMock()
    mock_weather.status_code = 500
    mock_weather.raise_for_status.side_effect = HTTPError("500 Server Error")

    mock_get.side_effect = [mock_geo, mock_weather]

    get_weather("Rome")

    captured = capsys.readouterr()
    assert "Errore di rete:" in captured.out


@patch('weather_script.requests.get')
def test_get_weather_empty_input(mock_get, capsys):
    """Test input vuoto."""
    get_weather("")

    captured = capsys.readouterr()
    assert "Errore: Nome città non valido." in captured.out
    mock_get.assert_not_called()


@patch('weather_script.requests.get')
def test_get_weather_whitespace_input(mock_get, capsys):
    """Test input con solo spazi."""
    get_weather("   ")

    captured = capsys.readouterr()
    assert "Errore: Nome città non valido." in captured.out
    mock_get.assert_not_called()


@patch('weather_script.requests.get')
def test_get_weather_network_timeout(mock_get, capsys):
    """Test eccezione di rete (timeout)."""
    from requests.exceptions import Timeout

    mock_get.side_effect = Timeout("Request timed out")

    get_weather("Rome")

    captured = capsys.readouterr()
    assert "Errore: timeout nella richiesta di rete." in captured.out


@patch('weather_script.requests.get')
def test_get_weather_malformed_json(mock_get, capsys):
    """Test JSON malformato."""
    import json

    mock_geo = MagicMock()
    mock_geo.status_code = 200
    mock_geo.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

    mock_get.return_value = mock_geo

    get_weather("Rome")

    captured = capsys.readouterr()
    assert "Errore: Risposta API non valida." in captured.out


@patch('weather_script.requests.get')
def test_get_weather_missing_keys(mock_get, capsys):
    """Test chiavi mancanti nel JSON."""
    mock_geo = MagicMock()
    mock_geo.status_code = 200
    mock_geo.json.return_value = [{"name": "Rome"}]

    mock_get.return_value = mock_geo

    get_weather("Rome")

    captured = capsys.readouterr()
    assert "Errore: Coordinate mancanti." in captured.out
