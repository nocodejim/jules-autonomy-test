from fastapi import FastAPI, Depends, HTTPException
import json
from app.cache import get_cache
import redis
from app.logging_config import setup_logging
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

setup_logging()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

from app.parser import parse_openapi
from app.inference import infer_schema_from_api

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/parse")
def parse_documentation(url: str, cache: redis.Redis = Depends(get_cache)):
    cached_result = cache.get(f"parse:{url}")
    if cached_result:
        return json.loads(cached_result)

    result = parse_openapi(url)
    cache.set(f"parse:{url}", json.dumps(result))
    return result

@app.post("/infer")
def infer_schema(api_description: str, cache: redis.Redis = Depends(get_cache)):
    cached_result = cache.get(f"infer:{api_description}")
    if cached_result:
        return json.loads(cached_result)

    result = infer_schema_from_api(api_description)
    cache.set(f"infer:{api_description}", json.dumps(result))
    return result

@app.post("/apis/", response_model=schemas.Api)
def create_api(api: schemas.ApiCreate, db: Session = Depends(get_db)):
    return crud.create_api(db=db, api=api)

@app.get("/apis/", response_model=list[schemas.Api])
def read_apis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apis = crud.get_apis(db, skip=skip, limit=limit)
    return apis

@app.get("/apis/{api_id}", response_model=schemas.Api)
def read_api(api_id: int, db: Session = Depends(get_db)):
    db_api = crud.get_api(db, api_id=api_id)
    if db_api is None:
        raise HTTPException(status_code=404, detail="Api not found")
    return db_api
