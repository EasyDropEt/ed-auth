from datetime import datetime
from typing import TypedDict
from uuid import UUID


class User(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    email: str
    password: str
    create_datetime: datetime
    update_datetime: datetime
