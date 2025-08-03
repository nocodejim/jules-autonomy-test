from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Api(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    schema = Column(JSON)
