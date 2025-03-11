from abc import ABCMeta

from ed_domain_model.entities import User

from src.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository


class ABCUserRepository(
    ABCGenericRepository[User],
    metaclass=ABCMeta,
): ...
