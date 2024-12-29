from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.user.dtos.user_dto import UserDto
from src.application.features.user.dtos.validators.login_dto_validator import (
    LoginDtoValidator,
)
from src.application.features.user.requests.commands.login_command import LoginCommand
from src.common.exception_helpers import ApplicationException, Exceptions
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginCommand, BaseResponse[UserDto])
class LoginCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: LoginCommand) -> BaseResponse[UserDto]:
        dto_validator = LoginDtoValidator().validate(request.dto)
        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Data is not valid",
                dto_validator.errors,
            )

        if user := self._uow.user_repository.get(
            email=request.dto.email, password=request.dto.password
        ):
            return BaseResponse.success(
                message="Login successful.",
                data=UserDto(name=user["name"], email=user["email"], role=user["role"]),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "User was not found.",
            ["User with email and password was not found."],
        )
