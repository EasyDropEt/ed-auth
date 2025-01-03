import uuid

from sqlalchemy import UUID, Column, String

from src.domain.entities.user import User
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.models.db_model import DbModel

db = DbClient()


class UserModel(db.Base, DbModel[User]):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(
            name=entity["name"],
            email=entity["email"],
            password=entity["password"],
            role=entity["role"],
        )

    @staticmethod
    def to_entity(model: "UserModel") -> User:
        uuid_str: str = str(model.id)
        return User(
            id=uuid.UUID(uuid_str),
            name=str(model.name),
            email=str(model.email),
            password=str(model.password),
            role=UserRole(model.role),
        )
