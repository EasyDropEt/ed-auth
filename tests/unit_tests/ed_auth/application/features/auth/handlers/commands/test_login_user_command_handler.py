from datetime import UTC, datetime

import pytest
from ed_domain.common.exceptions import ApplicationException

from ed_auth.application.features.auth.handlers.commands.login_user_command_handler import \
    LoginUserCommandHandler
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.handlers.commands.login_user_command_handler"

generate_fixtures(
    (f"{PATH}.ABCUnitOfWork", "mock_unit_of_work"),
    (f"{PATH}.ABCOtpGenerator", "mock_otp"),
    (f"{PATH}.ABCPasswordHandler", "mock_password"),
    (f"{PATH}.LoginUserCommand", "mock_login_user_command"),
    (f"{PATH}.LoginUserDtoValidator", "mock_login_user_dto_validator"),
)


@pytest.fixture
def handler(
    mock_unit_of_work,
    mock_otp,
    mock_password,
    mock_login_user_dto_validator,
):
    handler = LoginUserCommandHandler(
        uow=mock_unit_of_work, otp=mock_otp, password=mock_password
    )
    handler._dto_validator = mock_login_user_dto_validator

    return handler


@pytest.mark.asyncio
async def test_login_validation_failure(
    mock_unit_of_work,
    mock_otp,
    mock_password,
    mock_login_user_command,
    mock_login_user_dto_validator,
    handler,
):
    # Arrange
    mock_login_user_command.dto = {
        "email": "invalid-email",  # Invalid email format
        "password": "",  # Empty password
    }

    mock_login_user_dto_validator.validate.return_value.is_valid = False
    mock_login_user_dto_validator.validate.return_value.errors = [
        "Invalid email format",
        "Password is required",
    ]

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_login_user_command)

    assert "Login failed." == exc_info.value.message
    assert all(
        error in exc_info.value.errors
        for error in ["Invalid email format", "Password is required"]
    )
    mock_unit_of_work.auth_user_repository.get.assert_not_called()
    mock_unit_of_work.otp_repository.create.assert_not_called()
    mock_password.verify.assert_not_called()
    mock_otp.generate.assert_not_called()


@pytest.mark.asyncio
async def test_login_with_email_success(
    mock_unit_of_work, mock_otp, mock_password, mock_login_user_command, handler
):
    # Arrange
    mock_login_user_command.dto = {
        "email": "john.doe@example.com",
        "password": "securepassword",
    }

    mock_user = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "password_hash": "hashedpassword",
        "verified": True,
        "create_datetime": datetime.now(UTC),
        "update_datetime": datetime.now(UTC),
    }

    mock_unit_of_work.auth_user_repository.get.return_value = mock_user
    mock_password.verify.return_value = True
    mock_otp.generate.return_value = "123456"

    # Act
    response = await handler.handle(mock_login_user_command)

    # Assert
    assert response.is_success is True
    assert response.message == "Otp sent successfully."
    assert response.data["id"] == mock_user["id"]
    mock_unit_of_work.auth_user_repository.get.assert_called_once_with(
        email="john.doe@example.com"
    )
    mock_unit_of_work.otp_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_login_with_phone_success(
    mock_unit_of_work, mock_otp, mock_password, mock_login_user_command, handler
):
    # Arrange
    mock_login_user_command.dto = {
        "phone_number": "1234567890",
        "password": "securepassword",
    }

    mock_user = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "password_hash": "hashedpassword",
        "verified": True,
        "create_datetime": datetime.now(UTC),
        "update_datetime": datetime.now(UTC),
    }

    mock_unit_of_work.auth_user_repository.get.return_value = mock_user
    mock_password.verify.return_value = True
    mock_otp.generate.return_value = "123456"

    # Act
    response = await handler.handle(mock_login_user_command)

    # Assert
    assert response.is_success is True
    assert response.message == "Otp sent successfully."
    assert response.data["id"] == mock_user["id"]
    mock_unit_of_work.auth_user_repository.get.assert_called_once_with(
        phone_number="1234567890"
    )
    mock_unit_of_work.otp_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_login_user_not_found(
    mock_unit_of_work, mock_otp, mock_password, mock_login_user_command, handler
):
    # Arrange
    mock_login_user_command.dto = {
        "email": "nonexistent@example.com",
        "password": "securepassword",
    }

    mock_unit_of_work.auth_user_repository.get.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_login_user_command)

    assert "No user found with the given credentials." in str(
        exc_info.value.errors)


@pytest.mark.asyncio
async def test_login_missing_password(
    mock_unit_of_work, mock_otp, mock_password, mock_login_user_command, handler
):
    # Arrange
    mock_login_user_command.dto = {"email": "john.doe@example.com"}

    mock_user = {
        "id": "user-id",
        "email": "john.doe@example.com",
        "password_hash": "hashedpassword",
    }

    mock_unit_of_work.auth_user_repository.get.return_value = mock_user

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_login_user_command)

    assert "Password is required." in str(exc_info.value.errors)


@pytest.mark.asyncio
async def test_login_incorrect_password(
    mock_unit_of_work, mock_otp, mock_password, mock_login_user_command, handler
):
    # Arrange
    mock_login_user_command.dto = {
        "email": "john.doe@example.com",
        "password": "wrongpassword",
    }

    mock_user = {
        "id": "user-id",
        "email": "john.doe@example.com",
        "password_hash": "hashedpassword",
    }

    mock_unit_of_work.auth_user_repository.get.return_value = mock_user
    mock_password.verify.return_value = False

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_login_user_command)

    assert "Password is incorrect." in str(exc_info.value.errors)
