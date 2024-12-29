from dataclasses import dataclass

from src.domain.entities.user import UserRole


@dataclass
class UserDto:
    name: str
    email: str
    role: UserRole
