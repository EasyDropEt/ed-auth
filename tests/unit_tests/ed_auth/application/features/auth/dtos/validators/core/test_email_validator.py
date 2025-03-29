import pytest

from ed_auth.application.features.auth.dtos.validators.core.email_validator import (
    Email, EmailValidator)


@pytest.fixture
def email_validator():
    return EmailValidator()


def test_email_is_required(email_validator):
    dto = Email(value="")
    response = email_validator.validate(dto)
    assert not response.is_valid
    assert "Email is required." in response.errors


def test_invalid_email_format(email_validator):
    dto = Email(value="invalid-email")
    response = email_validator.validate(dto)
    assert not response.is_valid
    assert "Invalid email format." in response.errors


def test_valid_email(email_validator):
    dto = Email(value="test@example.com")
    response = email_validator.validate(dto)
    assert response.is_valid
    assert response.errors == []
