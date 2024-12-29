from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID


class UserRole(StrEnum):
    BUSINESS = "business"
    DRIVER = "driver"


class User(TypedDict):
    id: NotRequired[UUID]
    name: str
    email: str
    password: str
    role: UserRole
