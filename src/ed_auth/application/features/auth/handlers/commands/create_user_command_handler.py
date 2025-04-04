from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.entities import Otp, User
from ed_domain.core.entities.otp import OtpVerificationAction
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.utils.abc_otp import ABCOtp
from ed_auth.application.contracts.infrastructure.utils.abc_password import \
    ABCPassword
from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators import \
    CreateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    CreateUserCommand
from ed_auth.common.generic_helpers import get_new_id

LOG = get_logger()


@request_handler(CreateUserCommand, BaseResponse[UnverifiedUserDto])
class CreateUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, otp: ABCOtp, password: ABCPassword):
        self._uow = uow
        self._otp = otp
        self._password = password
        self._dto_validator = CreateUserDtoValidator()

    async def handle(
        self, request: CreateUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        validation_response = self._dto_validator.validate(request.dto)

        print(self._dto_validator)
        if not validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Creating account failed.",
                validation_response.errors,
            )

        dto = request.dto
        hashed_password = (
            self._password.hash(dto["password"]) if "password" in dto else ""
        )
        user = self._uow.user_repository.create(
            User(
                id=get_new_id(),
                first_name=dto["first_name"],
                last_name=dto["last_name"],
                email=dto.get("email", ""),
                phone_number=dto.get("phone_number", ""),
                password=hashed_password,
                verified=False,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
            )
        )

        self._uow.otp_repository.create(
            Otp(
                id=get_new_id(),
                user_id=user["id"],
                action=OtpVerificationAction.VERIFY_EMAIL,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                expiry_datetime=datetime.now(UTC),
                value=self._otp.generate(),
                deleted=False,
            )
        )

        return BaseResponse[UnverifiedUserDto].success(
            "Otp sent successfully.",
            UnverifiedUserDto(**user),  # type: ignore
        )
