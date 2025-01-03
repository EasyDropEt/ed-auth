from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID


class PaymentMethod(StrEnum):
    BANK_TRANSFER = "BANK_TRANSFER"
    TELEBIRR = "TELEBIRR"


class DriverPayment(TypedDict):
    amount: float
    status: str
    date: datetime
    payment_method: PaymentMethod


class Driver(TypedDict):
    id: UUID
    user_id: UUID
    car_id: UUID
    location_id: UUID
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    active_status: bool
    notification_ids: list[UUID]
    payment_history: list[DriverPayment]
    created_datetime: datetime
    updated_datetime: datetime
