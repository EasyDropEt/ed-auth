from rmediator.mediator import Mediator

from src.application.features.user.handlers.commands.some_command_handler import (
    SomeCommandHandler,
)
from src.application.features.user.requests.commands.some_command import SomeCommand
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork


def mediator() -> Mediator:
    # Dependencies
    db_client = DbClient()
    uow = UnitOfWork(db_client)

    # Setup
    mediator = Mediator()

    mediator.register_handler(SomeCommand, SomeCommandHandler(uow))

    db_client.start()
    return mediator
