from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.auth.dtos import UserDto, VerifyTokenDto


@request(BaseResponse[UserDto])
@dataclass
class VerifyTokenCommand(Request):
    dto: VerifyTokenDto
