from abc import ABCMeta

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)
from src.domain.entities.user import User


class ABCUserRepository(
    ABCGenericRepository[User],
    metaclass=ABCMeta,
): ...
