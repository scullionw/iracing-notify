from sqlalchemy.orm import Session

from . import models, schemas


def get_latest_result(db: Session):
    return db.query(models.Result).order_by(models.Result.id.desc()).first()


def create_result(db: Session, result: schemas.ResultCreate):
    db_result = models.Result(data=result.data)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
