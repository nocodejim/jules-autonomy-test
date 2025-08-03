from fastapi import FastAPI

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
def parse_documentation(url: str):
    return parse_openapi(url)

@app.post("/infer")
def infer_schema(api_description: str):
    return infer_schema_from_api(api_description)
