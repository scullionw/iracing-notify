from typing import List, Dict

from pydantic import BaseModel


# Info from outside that we also want inside
class ResultBase(BaseModel):
    data: List[dict]


# Info we get from outside but don't want inside
class ResultCreate(ResultBase):
    pass


# What we want to expose to outside that isn't in base or create
class Result(ResultBase):
    id: int

    class Config:
        orm_mode = True
