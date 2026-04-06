import requests
from app.models.weather import WeatherData
from app.config import Config  # Importa la configurazione per le chiavi API

def get_weather_data(city: str) -> WeatherData:
    # Esempio di uso della chiave API (se necessaria per future API)
    # api_key = Config.WEATHER_API_KEY
    # if not api_key:
    #     raise ValueError("Chiave API mancante")

    # Ottieni coordinate dalla città usando Nominatim (OpenStreetMap)
    geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    geo_response = requests.get(geo_url, headers={'User-Agent': 'WeatherApp/1.0'}, timeout=10)
    
    if geo_response.status_code != 200 or not geo_response.json():
        raise ValueError("Città non trovata")
    
    geo_data = geo_response.json()[0]
    lat = geo_data['lat']
    lon = geo_data['lon']
    
    # Ottieni dati meteo da Open-Meteo
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature,windspeed,weathercode,relative_humidity_2m,precipitation"
    weather_response = requests.get(weather_url, timeout=10)
    
    if weather_response.status_code != 200:
        raise ValueError("Impossibile recuperare i dati meteo")
    
    current_weather = weather_response.json()['current']
    
    return WeatherData(
        temperature=current_weather['temperature'],
        windspeed=current_weather['windspeed'],
        weathercode=current_weather['weathercode'],
        humidity=current_weather['relative_humidity_2m'],
        precipitation=current_weather['precipitation']
    )