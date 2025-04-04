from typing import Annotated

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.unit_of_work import UnitOfWork
from fastapi import Depends
from rmediator.mediator import Mediator

from ed_auth.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from ed_auth.application.contracts.infrastructure.utils.abc_otp import ABCOtp
from ed_auth.application.contracts.infrastructure.utils.abc_password import \
    ABCPassword
from ed_auth.application.features.auth.handlers.commands import (
    CreateUserCommandHandler, CreateUserVerifyCommandHandler,
    DeleteUserCommandHandler, LoginUserCommandHandler,
    LoginUserVerifyCommandHandler, VerifyTokenCommandHandler)
from ed_auth.application.features.auth.requests.commands import (
    CreateUserCommand, CreateUserVerifyCommand, DeleteUserCommand,
    LoginUserCommand, LoginUserVerifyCommand, VerifyTokenCommand)
from ed_auth.common.generic_helpers import get_config
from ed_auth.common.typing.config import Config
from ed_auth.infrastructure.utils.jwt import Jwt
from ed_auth.infrastructure.utils.otp import Otp
from ed_auth.infrastructure.utils.password import Password


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


def get_password(config: Annotated[Config, Depends(get_config)]) -> ABCPassword:
    return Password(config["password_scheme"])


def mediator(
    uow: Annotated[ABCUnitOfWork, Depends(get_uow)],
    jwt: Annotated[ABCJwt, Depends(get_jwt)],
    otp: Annotated[ABCOtp, Depends(get_otp)],
    password: Annotated[ABCPassword, Depends(get_password)],
) -> Mediator:
    mediator = Mediator()

    auth_handlers = [
        (CreateUserCommand, CreateUserCommandHandler(uow, otp, password)),
        (DeleteUserCommand, DeleteUserCommandHandler(uow)),
        (CreateUserVerifyCommand, CreateUserVerifyCommandHandler(uow, jwt)),
        (LoginUserCommand, LoginUserCommandHandler(uow, otp, password)),
        (LoginUserVerifyCommand, LoginUserVerifyCommandHandler(uow, jwt)),
        (VerifyTokenCommand, VerifyTokenCommandHandler(uow, jwt)),
    ]
    for request, handler in auth_handlers:
        mediator.register_handler(request, handler)

    return mediator
