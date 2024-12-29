from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.user.dtos.login_dto import LoginDto
from src.application.features.user.dtos.user_dto import UserDto


@request(BaseResponse[UserDto])
@dataclass
class LoginCommand(Request):
    dto: LoginDto
