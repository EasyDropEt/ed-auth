import pytest

from ed_auth.application.features.auth.dtos import CreateUserVerifyDto
from ed_auth.application.features.auth.dtos.validators.create_user_verify_dto_validator import \
    CreateUserVerifyDtoValidator
from tests.helpers.fixture_generator import generate_fixtures

PATH = (
    "ed_auth.application.features.auth.dtos.validators.create_user_verify_dto_validator"
)
generate_fixtures(
    (f"{PATH}.OtpValidator", "mock_otp_validator"),
)


@pytest.fixture
def create_user_verify_dto_validator(
    mock_otp_validator,
):
    validator = CreateUserVerifyDtoValidator()
    validator._otp_validator = mock_otp_validator

    return validator


def test_valid_create_user_verify_dto(create_user_verify_dto_validator):
    # Arrange
    dto = CreateUserVerifyDto(
        user_id="valid_user_id",
        otp="1234",
    )

    # Act
    response = create_user_verify_dto_validator.validate(dto)

    # Assert
    assert response.is_valid


def test_invalid_missing_user_id(create_user_verify_dto_validator):
    # Arrange
    dto = CreateUserVerifyDto(
        user_id="",
        otp="1234",
    )

    # Act
    response = create_user_verify_dto_validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in ["User ID is required"])


def test_invalid_missing_otp(create_user_verify_dto_validator, mock_otp_validator):
    # Arrange
    dto = CreateUserVerifyDto(
        user_id="valid_user_id",
        otp="",
    )
    mock_otp_validator.validate.return_value.is_valid = False
    mock_otp_validator.validate.return_value.errors = ["OTP is required"]

    # Act
    response = create_user_verify_dto_validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in ["OTP is required"])
