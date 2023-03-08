from pydantic import BaseModel
from typing import Any


class OCRResult(BaseModel):
    readable: bool = False
    confidence_score: float = 0.0
    readings: Any
    blurred: bool = False
    message: str = ""

    class Config:
        orm_mode = True



