import pytest

from ed_auth.application.features.auth.dtos.validators.core.phone_number_validator import (
    PhoneNumber, PhoneNumberValidator)


@pytest.fixture
def phone_number_validator():
    return PhoneNumberValidator()


def test_invalid_phone_number_empty(phone_number_validator):
    dto = PhoneNumber(value="")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is False
    assert "Phone number is required." in response.errors


def test_valid_phone_number_with_country_code(phone_number_validator):
    dto = PhoneNumber(value="+251912345678")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is True
    assert response.errors == []


def test_valid_phone_number_with_country_code_without_plus(phone_number_validator):
    dto = PhoneNumber(value="251912345678")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is True
    assert response.errors == []


def test_valid_phone_number_without_country_code(phone_number_validator):
    dto = PhoneNumber(value="0912345678")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is True
    assert response.errors == []


def test_invalid_phone_number_format(phone_number_validator):
    dto = PhoneNumber(value="123456")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is False
    assert "Invalid phone number format." in response.errors


def test_missing_phone_number(phone_number_validator):
    dto = PhoneNumber(value="")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is False
    assert "Phone number is required." in response.errors


def test_invalid_phone_number_with_letters(phone_number_validator):
    dto = PhoneNumber(value="09123abcde")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is False
    assert "Invalid phone number format." in response.errors


def test_invalid_phone_number_with_special_characters(phone_number_validator):
    dto = PhoneNumber(value="0912-345-678")
    response = phone_number_validator.validate(dto)
    assert response.is_valid is False
    assert "Invalid phone number format." in response.errors
