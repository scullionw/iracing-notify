from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from pydantic import BaseModel
from typing import List
import threading

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

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
            "series": "F3 Championship",
            "session_type": "Practice",
        },
    },
    {
        "name": "Charles Leclerc",
        "category": "F1",
        "driving": {
            "track": "Gilles-Villeneuve",
            "car": "Dallara F3",
            "series": "F3 Championship",
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
    series: str
    session_type: str


class Driver(BaseModel):
    name: str
    category: str
    driving: SessionInfo = None


@app.get("/api/drivers")
async def driver_status():
    return DRIVER_STATUS.value


@app.get("/test")
async def test():
    return "test"


@app.post("/api/update/")
async def update_driver_status(driverstatus: List[Driver]):
    DRIVER_STATUS.value = driverstatus
    return driverstatus


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
