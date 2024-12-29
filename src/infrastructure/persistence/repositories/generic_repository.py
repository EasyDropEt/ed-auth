from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)
from src.common.logging_helpers import get_logger
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.helpers import repository_class
from src.infrastructure.persistence.models.db_model import DbModel

T = TypeVar("T")

LOG = get_logger()


@repository_class
class GenericRepository(ABCGenericRepository[T], Generic[T]):
    def __init__(self, db: DbClient, model: type[DbModel]) -> None:
        self._db = db
        self._model = model

    def get_all(self, **filters: Any) -> list[T]:
        with Session(bind=self._db.Engine) as session:
            return list(
                map(
                    self._model.to_entity,
                    session.query(self._model).filter_by(**filters).all(),
                )
            )

    def get(self, **filters: Any) -> T | None:
        with Session(bind=self._db.Engine) as session:
            if found := session.query(self._model).filter_by(**filters).first():
                return self._model.to_entity(found)

    def create(self, entity: T) -> T:
        with Session(bind=self._db.Engine) as session:
            try:
                db_entity = self._model.from_entity(entity)
                session.add(db_entity)
                session.commit()
                session.refresh(db_entity)

                return self._model.to_entity(db_entity)

            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def update(self, id: UUID, entity: T) -> bool:
        with Session(bind=self._db.Engine) as session:
            try:
                db_entity = session.query(self._model).filter_by(id=id).first()
                if not db_entity:
                    return False

                for key, value in entity.__dict__:
                    setattr(db_entity, key, value)

                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def delete(self, id: UUID) -> bool:
        with Session(bind=self._db.Engine) as session:
            try:
                db_entity = session.query(self._model).filter_by(id=id).first()
                if not db_entity:
                    return False

                session.delete(db_entity)
                session.commit()
                return True

            except SQLAlchemyError as e:
                session.rollback()
                raise e
