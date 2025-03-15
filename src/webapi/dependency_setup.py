from typing import Annotated

from fastapi import Depends
from rmediator.mediator import Mediator

from src.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from src.application.contracts.infrastructure.utils.abc_otp import ABCOtp
from src.application.features.auth.handlers.commands import (
    CreateUserCommandHandler, CreateUserVerifyCommandHandler,
    DeleteUserCommandHandler, LoginUserCommandHandler,
    LoginUserVerifyCommandHandler, VerifyTokenCommandHandler)
from src.application.features.auth.requests.commands import (
    CreateUserCommand, CreateUserVerifyCommand, DeleteUserCommand,
    LoginUserCommand, LoginUserVerifyCommand, VerifyTokenCommand)
from src.common.generic_helpers import get_config
from src.common.typing.config import Config
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.utils.jwt import Jwt
from src.infrastructure.utils.otp import Otp


def get_uow(config: Annotated[Config, Depends(get_config)]) -> ABCUnitOfWork:
    db_client = DbClient(
        config["mongo_db_connection_string"],
        config["db_name"],
    )
    return UnitOfWork(db_client)


def get_jwt(config: Annotated[Config, Depends(get_config)]) -> ABCJwt:
    return Jwt(config["jwt_secret"], config["jwt_algorithm"])


def get_otp() -> ABCOtp:
    return Otp()


def mediator(
    uow: Annotated[ABCUnitOfWork, Depends(get_uow)],
    jwt: Annotated[ABCJwt, Depends(get_jwt)],
    otp: Annotated[ABCOtp, Depends(get_otp)],
) -> Mediator:
    mediator = Mediator()

    auth_handlers = [
        (CreateUserCommand, CreateUserCommandHandler(uow, otp)),
        (DeleteUserCommand, DeleteUserCommandHandler(uow)),
        (CreateUserVerifyCommand, CreateUserVerifyCommandHandler(uow, jwt)),
        (LoginUserCommand, LoginUserCommandHandler(uow, otp)),
        (LoginUserVerifyCommand, LoginUserVerifyCommandHandler(uow, jwt)),
        (VerifyTokenCommand, VerifyTokenCommandHandler(uow, jwt)),
    ]
    for request, handler in auth_handlers:
        mediator.register_handler(request, handler)

    return mediator
