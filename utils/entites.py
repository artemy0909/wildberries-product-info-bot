from dataclasses import field
from datetime import datetime

from pydantic import BaseModel


class ProductInfo(BaseModel):
    article: str
    title: str
    rating: float
    price: int
    quantity: int
    updated_at: datetime = field(default_factory=datetime.utcnow)


class ProductBody(BaseModel):
    article: str


class ResponseSchema(BaseModel):
    data: ProductInfo
    update_interval_minutes: int | None = None
