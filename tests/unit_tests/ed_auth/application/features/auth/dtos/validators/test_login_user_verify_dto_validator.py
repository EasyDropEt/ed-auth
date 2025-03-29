import pytest

from ed_auth.application.features.auth.dtos import LoginUserVerifyDto
from ed_auth.application.features.auth.dtos.validators.login_user_verify_dto_validator import \
    LoginUserVerifyDtoValidator
from tests.helpers.fixture_generator import generate_fixtures

PATH = (
    "ed_auth.application.features.auth.dtos.validators.login_user_verify_dto_validator"
)
generate_fixtures(
    (f"{PATH}.OtpValidator", "mock_otp_validator"),
)


@pytest.fixture
def login_user_verify_dto_validator(
    mock_otp_validator,
):
    validator = LoginUserVerifyDtoValidator()
    validator._otp_validator = mock_otp_validator

    return validator


def test_valid_login_user_verify_dto(login_user_verify_dto_validator):
    # Arrange
    dto = LoginUserVerifyDto(
        user_id="valid_user_id",
        otp="1234",
    )

    # Act
    response = login_user_verify_dto_validator.validate(dto)

    # Assert
    assert response.is_valid


def test_invalid_missing_user_id(login_user_verify_dto_validator):
    # Arrange
    dto = LoginUserVerifyDto(
        user_id="",
        otp="1234",
    )

    # Act
    response = login_user_verify_dto_validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in ["User ID is required"])


def test_invalid_missing_otp(login_user_verify_dto_validator, mock_otp_validator):
    # Arrange
    dto = LoginUserVerifyDto(
        user_id="valid_user_id",
        otp="",
    )
    mock_otp_validator.validate.return_value.is_valid = False
    mock_otp_validator.validate.return_value.errors = ["OTP is required"]

    # Act
    response = login_user_verify_dto_validator.validate(dto)

    # Assert
    assert all(error in response.errors for error in ["OTP is required"])
