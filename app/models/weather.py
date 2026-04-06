from pydantic import BaseModel

class WeatherData(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int
    humidity: float
    precipitation: float