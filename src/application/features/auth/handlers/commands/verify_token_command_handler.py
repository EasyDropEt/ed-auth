from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from src.application.features.auth.dtos import UserDto
from src.application.features.auth.requests.commands import VerifyTokenCommand
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(VerifyTokenCommand, BaseResponse[UserDto])
class VerifyTokenCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, jwt: ABCJwt):
        self._uow = uow
        self._jwt = jwt

    async def handle(self, request: VerifyTokenCommand) -> BaseResponse[UserDto]:
        payload = self._jwt.decode(request.dto["token"])

        return BaseResponse[UserDto].success(
            "Token validated.",
            UserDto(
                first_name=payload["first_name"],
                last_name=payload["last_name"],
                email=payload["email"],
                token=request.dto["token"],
            ),
        )
