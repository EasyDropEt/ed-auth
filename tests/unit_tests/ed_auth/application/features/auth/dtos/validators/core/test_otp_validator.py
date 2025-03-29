import pytest

from ed_auth.application.features.auth.dtos.validators.core.otp_validator import \
    OtpValidator


@pytest.fixture
def password_validator():
    return OtpValidator()


def test_valid_otp(password_validator):
    response = password_validator.validate({"value": "1234"})
    assert response.is_valid


@pytest.mark.parametrize(
    ["otp"],
    [
        ("12345",),
        ("123",),
    ],
)
def test_invalid_otp_invalid_length(otp, password_validator):
    response = password_validator.validate({"value": otp})
    assert not response.is_valid
    assert response.errors == ["OTP must be 4 numbers."]


@pytest.mark.parametrize(
    ["otp"],
    [
        ("abcd",),
        ("1a2b",),
        ("    ",),
    ],
)
def test_invalid_otp_non_numeric(otp, password_validator):
    response = password_validator.validate({"value": otp})
    assert not response.is_valid
    assert response.errors == ["OTP must be numeric."]
