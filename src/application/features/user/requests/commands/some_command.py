from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.user.dtos.some_create_dto import SomeCreateDto
from src.application.features.user.dtos.some_response_dto import SomeResponseDto


@request(BaseResponse[SomeResponseDto])
@dataclass
class SomeCommand(Request):
    dto: SomeCreateDto
