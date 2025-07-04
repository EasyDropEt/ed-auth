from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.persistence.async_repositories import ABCAsyncUnitOfWork
from ed_domain.utils.otp import ABCOtpGenerator
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators import \
    CreateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    CreateUserCommand
from ed_auth.application.services import OtpService, UserService

LOG = get_logger()


@request_handler(CreateUserCommand, BaseResponse[UnverifiedUserDto])
class CreateUserCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
        otp: ABCOtpGenerator,
        password: ABCPasswordHandler,
    ):
        self._uow = uow
        self._otp = otp

        self._dto_validator = CreateUserDtoValidator()
        self._user_service = UserService(uow, password)
        self._otp_service = OtpService(uow)

        self._success_message = "User account created successfully."
        self._error_message = "Creating account failed."

    async def handle(
        self, request: CreateUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        dto = request.dto
        dto_validation_response = self._dto_validator.validate(dto)

        if not dto_validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                self._error_message,
                dto_validation_response.errors,
            )

        async with self._uow.transaction():
            if "phone_number" in dto and await self._user_service.get_by_phone_number(
                dto["phone_number"]
            ):
                raise ApplicationException(
                    Exceptions.ConflictException,
                    self._error_message,
                    ["Another user exists with this phone number."],
                )

            # if "email" in dto and await self._user_service.get_by_email(dto["email"]):
            #     raise ApplicationException(
            #         Exceptions.ConflictException,
            #         self._error_message,
            #         ["Another user exists with this email."],
            #     )

            user = await self._user_service.create(request.dto)
            user_dto = await self._user_service.to_unverified_user_dto(user)

        return BaseResponse[UnverifiedUserDto].success(self._success_message, user_dto)
