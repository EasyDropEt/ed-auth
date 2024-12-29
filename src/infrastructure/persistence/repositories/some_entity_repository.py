from src.domain.entities.some_entity import SomeEntity
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.models.some_entity_model import SomeEntityModel
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class SomeEntityRepository(GenericRepository[SomeEntity]):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, SomeEntityModel)
