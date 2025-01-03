from typing import NotRequired, TypedDict


class CreateCarDto(TypedDict):
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str


class CreateLocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str


class CreateDriverDto(TypedDict):
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    password: str
    location: CreateLocationDto
    car: CreateCarDto
