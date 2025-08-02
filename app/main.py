from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

from app.parser import parse_openapi

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/parse")
def parse_documentation(url: str):
    return parse_openapi(url)
