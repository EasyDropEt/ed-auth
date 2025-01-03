from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.drivers.dtos.driver_dto import DriverDto
from src.application.features.drivers.requests.commands.create_driver_command import (
    CreateDriverCommand,
)
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateDriverCommand, BaseResponse[DriverDto])
class CreateDriverCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateDriverCommand) -> BaseResponse[DriverDto]: ...
