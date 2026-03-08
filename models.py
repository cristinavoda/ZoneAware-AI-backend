# backend/models.py
from pydantic import BaseModel
from typing import Optional

class Device(BaseModel):
    name: str
    phone_number: str
    lat: Optional[float] = None
    lon: Optional[float] = None