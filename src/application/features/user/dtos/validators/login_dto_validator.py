from src.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator,
    ValidationResponse,
)
from src.application.features.user.dtos.login_dto import LoginDto


class LoginDtoValidator(ABCDtoValidator[LoginDto]):
    def validate(self, dto: LoginDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
