from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.user.dtos.user_dto import UserDto
from src.application.features.user.dtos.validators.create_user_dto_validator import (
    CreateUserDtoValidator,
)
from src.application.features.user.requests.commands.create_user_command import (
    CreateUserCommand,
)
from src.common.exception_helpers import ApplicationException, Exceptions
from src.common.logging_helpers import get_logger
from src.domain.entities.user import User

LOG = get_logger()


@request_handler(CreateUserCommand, BaseResponse[UserDto])
class CreateUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateUserCommand) -> BaseResponse[UserDto]:
        dto_validator = CreateUserDtoValidator().validate(request.dto)
        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Data is not valid",
                dto_validator.errors,
            )

        created = self._uow.user_repository.create(
            User(
                name=request.dto.name,
                email=request.dto.email,
                role=request.dto.role,
                password=request.dto.password,
            )
        )

        return BaseResponse.success(
            message="Registration successful.",
            data=UserDto(
                name=created["name"], email=created["email"], role=created["role"]
            ),
        )
