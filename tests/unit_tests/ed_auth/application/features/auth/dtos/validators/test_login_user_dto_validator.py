import pytest

from ed_auth.application.features.auth.dtos import LoginUserDto
from ed_auth.application.features.auth.dtos.validators.login_user_dto_validator import \
    LoginUserDtoValidator
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.dtos.validators.login_user_dto_validator"
generate_fixtures(
    (f"{PATH}.EmailValidator", "mock_email_validator"),
    (f"{PATH}.PasswordValidator", "mock_password_validator"),
    (f"{PATH}.PhoneNumberValidator", "mock_phone_number_validator"),
)


@pytest.fixture
def validator(
    mock_email_validator,
    mock_password_validator,
    mock_phone_number_validator,
):
    validator = LoginUserDtoValidator()
    validator._email_validator = mock_email_validator
    validator._password_validator = mock_password_validator
    validator._phone_number_validator = mock_phone_number_validator

    return validator


def test_valid_login_user_dto(
    validator,
    mock_phone_number_validator,
    mock_email_validator,
    mock_password_validator,
):
    # Arrange
    dto = LoginUserDto(
        email="valid_email",
        phone_number="valid_phone_number",
        password="valid_password",
    )
    mock_phone_number_validator.validate.return_value.is_valid = True
    mock_email_validator.validate.return_value.is_valid = True
    mock_password_validator.validate.return_value.is_valid = True

    # Act
    response = validator.validate(dto)

    # Assert
    assert response.is_valid


def test_invalid_missing_email_and_phone_number(
    validator,
    mock_password_validator,
):
    # Arrange
    dto = LoginUserDto(
        password="valid_password",
    )
    mock_password_validator.validate.return_value.is_valid = True

    # Act
    response = validator.validate(dto)

    print(response.errors)
    # Assert
    assert all(
        error in response.errors
        for error in ["Either email or phone number must be provided"]
    )


def test_invalid_invalid_email(
    validator,
    mock_email_validator,
    mock_password_validator,
):
    # Arrange
    dto = LoginUserDto(
        email="invalid_email",
        phone_number="",
        password="valid_password",
    )
    mock_email_validator.validate.return_value.is_valid = False
    mock_email_validator.validate.return_value.errors = [
        "Invalid email format"]
    mock_password_validator.validate.return_value.is_valid = True

    # Act
    response = validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in ["Invalid email format"])


def test_invalid_invalid_phone_number(
    validator,
    mock_phone_number_validator,
    mock_password_validator,
):
    # Arrange
    dto = LoginUserDto(
        email="",
        phone_number="invalid_phone_number",
        password="valid_password",
    )
    mock_phone_number_validator.validate.return_value.is_valid = False
    mock_phone_number_validator.validate.return_value.errors = [
        "Invalid phone number format"
    ]
    mock_password_validator.validate.return_value.is_valid = True

    # Act
    response = validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in [
               "Invalid phone number format"])


def test_invalid_invalid_password(
    validator,
    mock_email_validator,
    mock_password_validator,
):
    # Arrange
    dto = LoginUserDto(
        email="valid_email",
        phone_number="",
        password="invalid_password",
    )
    mock_email_validator.validate.return_value.is_valid = True
    mock_password_validator.validate.return_value.is_valid = False
    mock_password_validator.validate.return_value.errors = [
        "Invalid password format"]

    # Act
    response = validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in [
               "Invalid password format"])
