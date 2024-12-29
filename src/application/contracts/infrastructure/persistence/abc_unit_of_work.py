from abc import ABCMeta, abstractmethod

from src.application.contracts.infrastructure.persistence.abc_user_repository import (
    ABCUserRepository,
)


class ABCUnitOfWork(metaclass=ABCMeta):
    @property
    @abstractmethod
    def user_repository(self) -> ABCUserRepository:
        pass
