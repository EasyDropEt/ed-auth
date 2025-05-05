import pytest

from ed_auth.application.features.auth.dtos import UpdateUserDto
from ed_auth.application.features.auth.dtos.validators.update_user_dto_validator import \
    UpdateUserDtoValidator
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.dtos.validators.update_user_dto_validator"
generate_fixtures(
    (f"{PATH}.EmailValidator", "mock_email_validator"),
    (f"{PATH}.PasswordValidator", "mock_password_validator"),
    (f"{PATH}.PhoneNumberValidator", "mock_phone_number_validator"),
)


@pytest.fixture
def update_user_dto_validator(
    mock_email_validator,
    mock_password_validator,
    mock_phone_number_validator,
):
    validator = UpdateUserDtoValidator()
    validator._email_validator = mock_email_validator
    validator._password_validator = mock_password_validator
    validator._phone_number_validator = mock_phone_number_validator

    return validator


def test_valid_update_user_dto(update_user_dto_validator):
    # Arrange
    dto = UpdateUserDto(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="1234567890",
        password="ValidPass123!",
    )

    # Act
    response = update_user_dto_validator.validate(dto)

    # Assert
    assert response.is_valid


def test_invalid_missing_email_and_phone(update_user_dto_validator):
    # Arrange
    dto = UpdateUserDto(
        first_name="John",
        last_name="Doe",
        password="ValidPass123!",
    )

    # Act
    response = update_user_dto_validator.validate(dto)

    # Assert
    assert all(
        error in response.errors
        for error in ["Either email or phone number must be provided"]
    )
