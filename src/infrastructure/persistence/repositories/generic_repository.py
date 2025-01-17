from typing import Any, Generic, TypeVar
from uuid import UUID

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)
from src.common.exception_helpers import ApplicationException, Exceptions
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.helpers import repository_class

TEntity = TypeVar("TEntity")


@repository_class
class GenericRepository(Generic[TEntity], ABCGenericRepository[TEntity]):
    def __init__(self, db: DbClient, collection: str) -> None:
        self._db = db.get_collection(f"{collection}s")
        self._collection = f"{collection[0].upper()}{collection[1:].lower()}"

    def get_all(self, **filters: Any) -> list[TEntity]:
        return list(self._db.find(filters))

    def get(self, **filters: Any) -> TEntity | None:
        if entity := self._db.find_one(filters):
            return entity

        return None

    def create(self, entity: TEntity) -> TEntity:
        if exists := self._db.find_one(entity):
            raise ApplicationException(
                Exceptions.BadRequestException,
                message=f"{self._collection} already exists.",
                errors=[f"{self._collection}: {exists} already exists"],
            )

        self._db.insert_one(entity)
        return entity

    def update(self, id: UUID, entity: TEntity) -> bool:
        status = self._db.update_one({"id": id}, {"$set": entity})
        return status.modified_count > 0

    def delete(self, id: UUID) -> bool:
        status = self._db.delete_one({"id": id})
        return status.deleted_count > 0
