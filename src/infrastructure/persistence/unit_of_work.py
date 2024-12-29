from src.application.contracts.infrastructure.persistence.abc_some_repository import (
    ABCSomeEntityRepository,
)
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.some_entity_repository import (
    SomeEntityRepository,
)


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, db_client: DbClient) -> None:
        self._some_entity_repository = SomeEntityRepository(db_client)

    @property
    def some_entity_repository(self) -> ABCSomeEntityRepository:
        return self._some_entity_repository
