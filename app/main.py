from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes import weather

app = FastAPI(title="App Meteo", description="App per visualizzare il meteo di una città")
templates = Jinja2Templates(directory="app/templates")

app.include_router(weather.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})