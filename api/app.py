from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import threading

app = FastAPI()


class AtomicValue:
    def __init__(self, value):
        self._value = value
        self._lock = threading.Lock()

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = v
            return self._value


DRIVER_STATUS_MOCK = [
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

DRIVER_STATUS = AtomicValue(DRIVER_STATUS_MOCK)


class SessionInfo(BaseModel):
    track: str
    car: str
    session_type: str


class Driver(BaseModel):
    name: str
    category: str
    driving: SessionInfo = None


@app.get("/api/drivers")
async def driver_status():
    return DRIVER_STATUS.value


@app.post("/api/update/")
async def update_driver_status(driverstatus: List[Driver]):
    DRIVER_STATUS.value = driverstatus
    return driverstatus
