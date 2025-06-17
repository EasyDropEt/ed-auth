from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.jwt import ABCJwtHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import UserDto
from ed_auth.application.features.auth.requests.commands import \
    VerifyTokenCommand

LOG = get_logger()


@request_handler(VerifyTokenCommand, BaseResponse[UserDto])
class VerifyTokenCommandHandler(RequestHandler):
    def __init__(self, uow: ABCAsyncUnitOfWork, jwt: ABCJwtHandler):
        self._uow = uow
        self._jwt = jwt

        self._error_message = "Token validation failed."
        self._success_message = "Token validated."

    async def handle(self, request: VerifyTokenCommand) -> BaseResponse[UserDto]:
        payload = self._jwt.decode(request.dto["token"])

        if "email" not in payload:
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                self._error_message,
                ["Token is malformed."],
            )

        async with self._uow.transaction():
            user = await self._uow.auth_user_repository.get(
                phone_number=payload["phone_number"]
            )

            if user is None:
                raise ApplicationException(
                    Exceptions.UnauthorizedException,
                    self._error_message,
                    ["User not found."],
                )

            if not user.logged_in:
                raise ApplicationException(
                    Exceptions.UnauthorizedException,
                    self._error_message,
                    ["User is not logged in."],
                )

            return BaseResponse[UserDto].success(
                self._success_message,
                UserDto(**user.__dict__, token=request.dto["token"]),
            )
