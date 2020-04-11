from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from pydantic import BaseModel
from typing import List, Dict, Any
import threading
import time

from . import crud, models, schemas
from .database import SessionLocal, engine


def wait_for_db():
    while True:
        try:
            models.Base.metadata.create_all(bind=engine)
        except:
            print("Database is down.. waiting")
            time.sleep(1)
        else:
            print("Connected to database!")
            break


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


wait_for_db()

app = FastAPI()


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
def driver_status(db: Session = Depends(get_db)):
    latest = crud.get_latest_result(db)
    if latest:
        return latest.data
    else:
        return None


@app.post("/api/update/")
def update_driver_status(driverstatus: List[Driver], db: Session = Depends(get_db)):
    return crud.create_result(
        db, schemas.ResultCreate(data=jsonable_encoder(driverstatus))
    )
