import os
from dotenv import load_dotenv

load_dotenv()  # Carica le variabili dal file .env

class Config:
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    # Aggiungi qui altre configurazioni se necessarie