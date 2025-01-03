from rmediator.mediator import Mediator

from src.application.features.drivers.handlers.commands import (
    CreateDriverCommandHandler,
    LoginDriverCommandHandler,
)
from src.application.features.drivers.requests.commands import (
    CreateDriverCommand,
    LoginDriverCommand,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork


def mediator() -> Mediator:
    # Dependencies
    db_client = DbClient()
    uow = UnitOfWork(db_client)

    # Setup
    mediator = Mediator()

    mediator.register_handler(CreateDriverCommand, CreateDriverCommandHandler(uow))
    mediator.register_handler(LoginDriverCommand, LoginDriverCommandHandler(uow))

    db_client.start()
    return mediator
