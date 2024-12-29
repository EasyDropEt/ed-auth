from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.user.dtos.some_response_dto import SomeResponseDto
from src.application.features.user.dtos.validators.some_dto_validator import (
    SomeDtoValidator,
)
from src.application.features.user.requests.commands.some_command import SomeCommand
from src.common.exception_helpers import ApplicationException, Exceptions
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(SomeCommand, BaseResponse[SomeResponseDto])
class SomeCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: SomeCommand) -> BaseResponse[SomeResponseDto]:
        dto_validator = SomeDtoValidator().validate(request.dto)

        if dto_validator.is_valid:
            return BaseResponse.success(
                message="Some response message.", data=SomeResponseDto(request.dto.data)
            )

        raise ApplicationException(
            Exceptions.ValidationException,
            "Data is not valid",
            dto_validator.errors,
        )
