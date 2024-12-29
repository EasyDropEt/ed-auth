from rmediator.mediator import Mediator

from src.application.features.user.handlers.commands.create_user_command_handler import (
    CreateUserCommandHandler,
)
from src.application.features.user.handlers.commands.login_command_handler import (
    LoginCommandHandler,
)
from src.application.features.user.requests.commands.create_user_command import (
    CreateUserCommand,
)
from src.application.features.user.requests.commands.login_command import LoginCommand
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork


def mediator() -> Mediator:
    # Dependencies
    db_client = DbClient()
    uow = UnitOfWork(db_client)

    # Setup
    mediator = Mediator()

    mediator.register_handler(CreateUserCommand, CreateUserCommandHandler(uow))
    mediator.register_handler(LoginCommand, LoginCommandHandler(uow))

    db_client.start()
    return mediator
