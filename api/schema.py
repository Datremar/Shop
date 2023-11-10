from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from models import Gender


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    patronymic: str
    surname: str
    year: int
    gender: Gender
    email: str
    consent: bool
    registered_at: Optional[datetime] = None

    @field_validator('consent')
    @classmethod
    def consent_true(cls, consent):
        if not consent:
            raise ValueError("Consent should always be true")

        return consent


class GoodSchema(BaseModel):
    id: Optional[int] = None
    name: str
    buy_price: float
    sell_price: float


class PurchaseSchema(BaseModel):
    id: Optional[int] = None
    buyer_id: int
    purchased_at: Optional[datetime] = None


class PurchaseEntrySchema(BaseModel):
    id: Optional[int] = None

    item_id: int
    item_quantity: int
    summary_price: Optional[float] = None

    purchase_id: int

    @field_validator('item_quantity')
    @classmethod
    def quantity_not_negative(cls, item_quantity):
        if item_quantity < 0:
            raise ValueError("Item quantity can't be negative")

        return item_quantity


class ReportSchema(BaseModel):
    id: int
    name: str
    email: str
    total: float
