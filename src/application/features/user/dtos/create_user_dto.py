from dataclasses import dataclass

from src.domain.entities.user import UserRole


@dataclass
class CreateUserDto:
    name: str
    email: str
    password: str
    role: UserRole
