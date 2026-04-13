import json
import requests

def get_weather(city_name):
    """
    Recupera e visualizza la temperatura attuale per una città specificata.

    Questa funzione utilizza l'API Nominatim (OpenStreetMap) per ottenere le coordinate
    geografiche della città e l'API Open-Meteo per recuperare i dati meteorologici attuali.
    In caso di successo, stampa la temperatura in gradi Celsius sulla console.
    Gestisce vari tipi di errori (input non valido, città non trovata, problemi di rete)
    stampando messaggi di errore appropriati.

    Args:
        city_name (str): Il nome della città per cui ottenere il meteo.
                         Deve essere una stringa non vuota e valida.

    Returns:
        None: La funzione non restituisce valori, ma produce output sulla console.

    Raises:
        Non solleva eccezioni direttamente, ma cattura e gestisce internamente:
        - Timeout delle richieste di rete
        - Errori di connessione o risposta HTTP
        - Risposte JSON non valide
        - Eccezioni generiche impreviste

    Example:
        >>> get_weather("Roma")
        La temperatura attuale a Roma è di 18.5°C.

        >>> get_weather("")
        Errore: Nome città non valido.
    """
    if not isinstance(city_name, str) or not city_name.strip():
        print("Errore: Nome città non valido.")
        return

    try:
        # Passo 1: Ottieni le coordinate della città usando Nominatim
        geo_url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
        geo_response = requests.get(geo_url, headers={'User-Agent': 'WeatherScript/1.0'}, timeout=10)
        geo_response.raise_for_status()

        geo_data = geo_response.json()
        if not geo_data:
            print("Errore: Città non trovata.")
            return

        geo_item = geo_data[0]
        lat = geo_item.get('lat')
        lon = geo_item.get('lon')
        if not lat or not lon:
            print("Errore: Coordinate mancanti.")
            return

        # Passo 2: Ottieni i dati meteo da Open-Meteo
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature,windspeed,weathercode,relative_humidity_2m,precipitation"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current_weather = weather_data.get('current')
        if not current_weather:
            print("Errore: Dati meteo non disponibili.")
            return

        temperature = current_weather.get('temperature')
        windspeed = current_weather.get('windspeed')
        weathercode = current_weather.get('weathercode')
        humidity = current_weather.get('relative_humidity_2m')
        precipitation = current_weather.get('precipitation')

        if temperature is None:
            print("Errore: Temperatura non disponibile.")
            return

        # Passo 3: Stampa i dati meteo
        print(f"Meteo attuale a {city_name}:")
        print(f"Temperatura: {temperature}°C")
        print(f"Velocità del vento: {windspeed} km/h")
        print(f"Umidità: {humidity}%")
        print(f"Precipitazioni: {precipitation} mm")
        print(f"Codice meteo: {weathercode} (vedi legenda Open-Meteo per descrizione)")

    except requests.exceptions.Timeout:
        print("Errore: timeout nella richiesta di rete.")
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
    except json.JSONDecodeError:
        print("Errore: Risposta API non valida.")
    except Exception as e:
        print(f"Errore inaspettato: {e}")

# Esegui lo script
if __name__ == "__main__":
    city = input("Inserisci il nome della città: ")
    get_weather(city)