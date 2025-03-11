from src.application.contracts.infrastructure.persistence.abc_otp_repository import \
    ABCOtpRepository
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.application.contracts.infrastructure.persistence.abc_user_repository import \
    ABCUserRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.otp_repository import \
    OtpRepository
from src.infrastructure.persistence.repositories.user_repository import \
    UserRepository


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, db_client: DbClient) -> None:
        self._otp_repository = OtpRepository(db_client)
        self._user_repository = UserRepository(db_client)

    @property
    def user_repository(self) -> ABCUserRepository:
        return self._user_repository

    @property
    def otp_repository(self) -> ABCOtpRepository:
        return self._otp_repository
