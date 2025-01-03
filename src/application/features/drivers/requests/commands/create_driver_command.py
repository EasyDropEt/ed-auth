from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.drivers.dtos.create_driver_dto import CreateDriverDto
from src.application.features.drivers.dtos.driver_dto import DriverDto


@request(BaseResponse[DriverDto])
@dataclass
class CreateDriverCommand(Request):
    dto: CreateDriverDto
