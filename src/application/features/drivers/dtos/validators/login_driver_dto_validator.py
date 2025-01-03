from src.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator,
    ValidationResponse,
)
from src.application.features.drivers.dtos.login_driver_dto import LoginDriverDto


class LoginDriverDtoValidator(ABCDtoValidator[LoginDriverDto]):
    def validate(self, dto: LoginDriverDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
