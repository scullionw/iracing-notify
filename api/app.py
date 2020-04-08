from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

DRIVER_STATUS = [
    {
        "name": "Max Verstappen",
        "category": "F1",
        "driving": {
            "track": "Gilles-Villeneuve",
            "car": "Dallara F3",
            "session_type": "Practice",
        },
    },
    {
        "name": "Charles Leclerc",
        "category": "F1",
        "driving": {
            "track": "Gilles-Villeneuve",
            "car": "Dallara F3",
            "session_type": "Practice",
        },
    },
    {"name": "Lando Norris", "category": "F1", "driving": None},
    {"name": "Suellio Almeida", "category": "Sim", "driving": None},
]


class SessionInfo(BaseModel):
    track: str
    car: str
    session_type: str


class Driver(BaseModel):
    name: str
    category: str
    driving: SessionInfo


@app.get("/api/drivers")
async def driver_status():
    return DRIVER_STATUS


@app.post("/api/update/")
async def update_driver_status(driverstatus: List[Driver]):
    return driverstatus
