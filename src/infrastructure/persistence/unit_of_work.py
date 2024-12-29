from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.contracts.infrastructure.persistence.abc_user_repository import (
    ABCUserRepository,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.user_repository import UserRepository


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, db_client: DbClient) -> None:
        self._user_repository = UserRepository(db_client)

    @property
    def user_repository(self) -> ABCUserRepository:
        return self._user_repository
