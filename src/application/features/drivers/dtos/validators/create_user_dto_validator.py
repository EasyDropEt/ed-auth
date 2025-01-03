from src.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator,
    ValidationResponse,
)
from src.application.features.user.dtos.create_user_dto import CreateUserDto


class CreateUserDtoValidator(ABCDtoValidator[CreateUserDto]):
    def validate(self, dto: CreateUserDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
