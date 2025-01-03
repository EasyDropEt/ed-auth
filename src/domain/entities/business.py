from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Business(TypedDict):
    id: UUID
    location_id: UUID
    user_id: UUID
    notification_ids: list[UUID]
    business_name: str
    owner_first_name: str
    owner_last_name: str
    email: str
    phone_number: str
    registration_date: datetime
    billing_details: str
    active_status: bool
