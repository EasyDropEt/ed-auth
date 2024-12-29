from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from src.common.singleton_helpers import SingletonMeta


class DbClient(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._base = declarative_base()
        self._engine = create_engine(
            "postgresql://easydrop:easydrop@localhost:5432/easydrop"
        )
        self._is_started = False

    @property
    def Base(self):
        return self._base

    @property
    def Engine(self):
        assert self._is_started, "DbClient is not started"
        return self._engine

    def start(self) -> None:
        self._base.metadata.create_all(self._engine)
        self._is_started = True

    def stop(self) -> None:
        self._engine.dispose()
