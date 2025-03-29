import pytest

from ed_auth.application.features.auth.dtos import CreateUserDto
from ed_auth.application.features.auth.dtos.validators.create_user_dto_validator import \
    CreateUserDtoValidator
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.dtos.validators.create_user_dto_validator"
generate_fixtures(
    (f"{PATH}.EmailValidator", "mock_email_validator"),
    (f"{PATH}.PasswordValidator", "mock_password_validator"),
    (f"{PATH}.PhoneNumberValidator", "mock_phone_number_validator"),
)


@pytest.fixture
def create_user_dto_validator(
    mock_email_validator,
    mock_password_validator,
    mock_phone_number_validator,
):
    validator = CreateUserDtoValidator()
    validator._email_validator = mock_email_validator
    validator._password_validator = mock_password_validator
    validator._phone_number_validator = mock_phone_number_validator

    return validator


def test_valid_create_user_dto(create_user_dto_validator):
    # Arrange
    dto = CreateUserDto(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="1234567890",
        password="ValidPass123!",
    )

    # Act
    response = create_user_dto_validator.validate(dto)

    # Assert
    assert response.is_valid


def test_invalid_missing_first_name(create_user_dto_validator):
    # Arrange
    dto = CreateUserDto(
        first_name="",
        last_name="Doe",
        email="john.doe@example.com",
    )

    # Act
    response = create_user_dto_validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in [
               "First name is required"])


def test_invalid_missing_last_name(create_user_dto_validator):
    # Arrange
    dto = CreateUserDto(
        first_name="John",
        last_name="",
        email="john.doe@example.com",
    )

    # Act
    response = create_user_dto_validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in ["Last name is required"])


def test_invalid_missing_email_and_phone(create_user_dto_validator):
    # Arrange
    dto = CreateUserDto(
        first_name="John",
        last_name="Doe",
        email=None,
        phone_number=None,
        password="ValidPass123!",
    )

    # Act
    response = create_user_dto_validator.validate(dto)

    # Assert
    assert all(
        error in response.errors
        for error in ["Either email or phone number must be provided"]
    )
