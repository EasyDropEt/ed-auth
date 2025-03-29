import pytest

from ed_auth.application.features.auth.dtos.validators.core.password_validator import (
    Password, PasswordValidator)


@pytest.fixture
def password_validator():
    return PasswordValidator()


def test_password_is_required(password_validator):
    dto = Password(value="")
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert "Password is required." in response.errors


def test_password_minimum_length(password_validator):
    dto = Password(value="Ab1!")
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert "Password must be at least 8 characters long." in response.errors


def test_password_must_include_number(password_validator):
    dto = Password(value="Abcdefgh!")
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert "Password must include at least one number." in response.errors


def test_password_must_include_uppercase(password_validator):
    dto = Password(value="abcdefgh1!")
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert "Password must include at least one uppercase letter." in response.errors


def test_password_must_include_lowercase(password_validator):
    dto = Password(value="ABCDEFGH1!")
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert "Password must include at least one lowercase letter." in response.errors


def test_password_must_include_special_character(password_validator):
    dto = Password(value="Abcdefgh1")
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert (
        "Password must include at least one special character (!@#$%^&*()-_+=)."
        in response.errors
    )


def test_valid_password(password_validator):
    dto = Password(value="Abcdef1!")
    response = password_validator.validate(dto)
    assert response.is_valid
    assert response.errors == []
