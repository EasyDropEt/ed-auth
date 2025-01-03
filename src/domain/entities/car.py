from typing import TypedDict
from uuid import UUID


class Car(TypedDict):
    id: UUID
    driver_id: UUID
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str
