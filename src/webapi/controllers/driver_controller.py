from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.drivers.dtos import (
    CreateDriverDto,
    DriverDto,
    LoginDriverDto,
)
from src.application.features.drivers.requests.commands import (
    CreateDriverCommand,
    LoginDriverCommand,
)
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

ROUTER = APIRouter(prefix="/drivers", tags=["Driver Feature"])
LOG = get_logger()


@ROUTER.post("/create", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def create_driver(
    request_dto: CreateDriverDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(CreateDriverCommand(dto=request_dto))


@ROUTER.post("/login", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def login_driver(
    request_dto: LoginDriverDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(LoginDriverCommand(dto=request_dto))
