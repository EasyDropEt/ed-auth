from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.user.dtos.create_user_dto import CreateUserDto
from src.application.features.user.dtos.login_dto import LoginDto
from src.application.features.user.dtos.user_dto import UserDto
from src.application.features.user.requests.commands.create_user_command import (
    CreateUserCommand,
)
from src.application.features.user.requests.commands.login_command import LoginCommand
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/user", tags=["User Feature"])


@router.post("/register", response_model=GenericResponse[UserDto])
@rest_endpoint
async def register(
    request_dto: CreateUserDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(CreateUserCommand(dto=request_dto))


@router.post("/login", response_model=GenericResponse[UserDto])
@rest_endpoint
async def login(
    request_dto: LoginDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(LoginCommand(dto=request_dto))
