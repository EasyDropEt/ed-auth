from ed_domain_model.entities import User

from src.application.contracts.infrastructure.persistence.abc_user_repository import \
    ABCUserRepository
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.repositories.generic_repository import \
    GenericRepository


class UserRepository(GenericRepository[User], ABCUserRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "user")
