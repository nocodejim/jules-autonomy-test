from sqlalchemy.orm import Session
from . import models, schemas

def get_api(db: Session, api_id: int):
    return db.query(models.Api).filter(models.Api.id == api_id).first()

def get_apis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Api).offset(skip).limit(limit).all()

def create_api(db: Session, api: schemas.ApiCreate):
    db_api = models.Api(**api.dict())
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api
