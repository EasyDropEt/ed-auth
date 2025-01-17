from ed_domain_model.entities.otp import Otp

from src.application.contracts.infrastructure.persistence.abc_otp_repository import (
    ABCOtpRepository,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class OtpRepository(GenericRepository[Otp], ABCOtpRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "otp")
