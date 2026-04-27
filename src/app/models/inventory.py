from datetime import date

from pydantic import BaseModel


class ItemBody(BaseModel):
    name: str
    price: int
    expiry_date: date
