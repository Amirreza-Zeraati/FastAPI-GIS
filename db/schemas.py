from pydantic import BaseModel
from typing import Optional


class GPS(BaseModel):
    longitude: float
    latitude: float
    message: str = "Marker"
    group: Optional[int] = 0
