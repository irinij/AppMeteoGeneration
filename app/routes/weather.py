from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.weather_service import get_weather_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str):
    try:
        weather = get_weather_data(city)
        weather_descriptions = {
            0: 'Cielo sereno',
            1: 'Prevalentemente sereno',
            2: 'Parzialmente nuvoloso',
            3: 'Coperto',
            45: 'Nebbia',
            48: 'Nebbia con brina depositata',
            51: 'Pioviggine leggera',
            53: 'Pioviggine moderata',
            55: 'Pioviggine densa',
            56: 'Pioviggine ghiacciata leggera',
            57: 'Pioviggine ghiacciata densa',
            61: 'Pioggia leggera',
            63: 'Pioggia moderata',
            65: 'Pioggia intensa',
            66: 'Pioggia ghiacciata leggera',
            67: 'Pioggia ghiacciata densa',
            71: 'Neve leggera',
            73: 'Neve moderata',
            75: 'Neve intensa',
            77: 'Granuli di neve',
            80: 'Pioggia leggera a rovesci',
            81: 'Pioggia moderata a rovesci',
            82: 'Pioggia intensa a rovesci',
            85: 'Neve leggera a rovesci',
            86: 'Neve intensa a rovesci',
            95: 'Temporale',
            96: 'Temporale con grandine leggera',
            99: 'Temporale con grandine intensa'
        }
        description = weather_descriptions.get(weather.weathercode, 'Descrizione meteo non disponibile')
        return templates.TemplateResponse(
            request,
            "weather.html",
            {
                "request": request,
                "weather": weather.model_dump(),
                "city": city,
                "weather_description": description,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))