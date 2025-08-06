from pydantic import BaseModel
from typing import Dict, Any

class ApiBase(BaseModel):
    name: str
    description: str | None = None
    schema: Dict[str, Any]

class ApiCreate(ApiBase):
    pass

class Api(ApiBase):
    id: int

    class Config:
        orm_mode = True
