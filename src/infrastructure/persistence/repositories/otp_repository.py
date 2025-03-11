from typing import override

from ed_domain_model.entities.otp import Otp

from src.application.contracts.infrastructure.persistence.abc_otp_repository import \
    ABCOtpRepository
from src.common.exception_helpers import ApplicationException, Exceptions
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import \
    GenericRepository


class OtpRepository(GenericRepository[Otp], ABCOtpRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "otp")

    @override
    def create(self, entity: Otp) -> Otp:
        existing_entity = self._db.find_one({"user_id": entity["user_id"]})
        if existing_entity:
            self._db.delete_one({"user_id": entity["user_id"]})

        if exists := self._db.find_one(entity):
            raise ApplicationException(
                Exceptions.BadRequestException,
                message=f"{self._collection} already exists.",
                errors=[f"{self._collection}: {exists} already exists"],
            )

        self._db.insert_one(entity)
        return entity
