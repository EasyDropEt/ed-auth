from abc import ABCMeta

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)
from src.domain.entities.some_entity import SomeEntity


class ABCSomeEntityRepository(
    ABCGenericRepository[SomeEntity],
    metaclass=ABCMeta,
): ...
