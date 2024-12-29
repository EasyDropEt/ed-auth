from dataclasses import dataclass

from src.domain.entities.some_entity import SomeEntity


@dataclass
class SomeResponseDto:
    data: str
