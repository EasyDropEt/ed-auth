from ed_domain_model.entities.otp import OtpVerificationAction
from ed_domain_model.tokens.auth_payload import UserType
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from src.application.features.auth.dtos import UserDto
from src.application.features.auth.dtos.create_user_verify_dto import \
    CreateUserVerifyDto
from src.application.features.auth.dtos.validators.verify_otp_dto_validator import \
    VerifyOtpDtoValidator
from src.application.features.auth.requests.commands import \
    CreateUserVerifyCommand
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateUserVerifyCommand, BaseResponse[UserDto])
class CreateUserVerifyCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, jwt: ABCJwt):
        self._uow = uow
        self._jwt = jwt

    async def handle(self, request: CreateUserVerifyCommand) -> BaseResponse[UserDto]:
        dto_validator = VerifyOtpDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[UserDto].error(
                "Otp verification failed.", dto_validator.errors
            )

        dto: CreateUserVerifyDto = request.dto
        user = self._uow.user_repository.get(id=dto["user_id"])
        if not user:
            return BaseResponse[UserDto].error(
                "Otp verification failed.",
                [f"User with that id = {dto['user_id']} does not exist."],
            )

        otp = self._uow.otp_repository.get(user_id=dto["user_id"])
        if not otp or otp["value"] != OtpVerificationAction.VERIFY_EMAIL:
            return BaseResponse[UserDto].error(
                "Otp verification failed.",
                [
                    f"Otp has not been sent to the user with id = {dto['user_id']} recently."
                ],
            )

        if otp["value"] != dto["otp"]:
            return BaseResponse[UserDto].error(
                "Otp verification failed.",
                ["Otp does not match with the one sent."],
            )

        return BaseResponse[UserDto].success(
            "Create successful.",
            UserDto(
                **user,  # type: ignore
                token=self._jwt.encode(
                    {
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "email": user.get("email", ""),
                        "phone_number": user.get("phone_number", ""),
                        "user_type": UserType.DRIVER,
                    }
                ),
            ),
        )
