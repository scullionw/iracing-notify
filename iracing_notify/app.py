from fastapi import FastAPI

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
    {"name": "Lando Norris", "category": "F1", "driving": None},
    {"name": "Suellio Almeida", "category": "Sim", "driving": None},
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/drivers")
def driver_status():
    return DRIVER_STATUS
