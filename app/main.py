from fastapi import FastAPI, Depends
import json
from app.cache import get_cache
import redis
from app.logging_config import setup_logging

setup_logging()

app = FastAPI()

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
