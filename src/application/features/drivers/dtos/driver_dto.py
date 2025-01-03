from typing import NotRequired, TypedDict

from src.domain.entities.driver import DriverPayment


class CarDto(TypedDict):
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str


class LocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str


class DriverDto(TypedDict):
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    car: CarDto
    location: LocationDto
    payment_history: list[DriverPayment]
