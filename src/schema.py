from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class TireInfo(BaseModel):
    type: Literal["brand-new", "used", "other"]
    manufactured_year: int

class Notice(BaseModel):
    type: str
    description: str

class PriceInfo(BaseModel):
    amount: int
    currency: str

class Car(BaseModel):
    body_type: Optional[str]
    color: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    manufactured_year: Optional[int]
    motor_size_cc: Optional[int]
    tires: Optional[TireInfo]
    windows: Optional[str]
    notices: List[Notice] = []
    price: Optional[PriceInfo] = None
    class Config:
        extra = "forbid"

class CarListing(BaseModel):
    car: Car
