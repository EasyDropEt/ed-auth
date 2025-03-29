import pytest
from ed_domain.entities.otp import OtpVerificationAction
from ed_domain.tokens.auth_payload import UserType

from ed_auth.application.features.auth.handlers.commands.create_user_verify_command_handler import \
    CreateUserVerifyCommandHandler
from ed_auth.common.exception_helpers import ApplicationException
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.handlers.commands.create_user_verify_command_handler"

generate_fixtures(
    (f"{PATH}.ABCUnitOfWork", "mock_unit_of_work"),
    (f"{PATH}.ABCJwt", "mock_jwt"),
    (f"{PATH}.CreateUserVerifyCommand", "mock_create_user_verify_command"),
    (f"{PATH}.CreateUserVerifyDtoValidator",
     "mock_create_user_verify_dto_validator"),
)


@pytest.fixture
def handler(
    mock_unit_of_work,
    mock_jwt,
    mock_create_user_verify_dto_validator,
):
    handler = CreateUserVerifyCommandHandler(
        uow=mock_unit_of_work,
        jwt=mock_jwt,
    )
    handler._dto_validator = mock_create_user_verify_dto_validator

    return handler


@pytest.mark.asyncio
async def test_create_user_verify_validation_failure(
    mock_unit_of_work,
    mock_jwt,
    mock_create_user_verify_command,
    mock_create_user_verify_dto_validator,
    handler,
):
    # Arrange
    mock_create_user_verify_command.dto = {
        "user_id": "",  # Invalid: empty user_id
        "otp": "123",  # Invalid: too short
    }

    mock_create_user_verify_dto_validator.validate.return_value.is_valid = False
    mock_create_user_verify_dto_validator.validate.return_value.errors = [
        "User ID is required",
        "OTP must be 4 digits",
    ]

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_create_user_verify_command)

    assert "Otp verification failed." == exc_info.value.message
    assert all(
        error in exc_info.value.errors
        for error in ["User ID is required", "OTP must be 4 digits"]
    )
    mock_unit_of_work.user_repository.get.assert_not_called()
    mock_unit_of_work.otp_repository.get.assert_not_called()
    mock_jwt.encode.assert_not_called()


@pytest.mark.asyncio
async def test_create_user_verify_success(
    mock_unit_of_work, mock_jwt, mock_create_user_verify_command, handler
):
    # Arrange
    mock_user = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "verified": False,
    }

    mock_otp = {
        "user_id": "user-id",
        "value": "1234",
        "action": OtpVerificationAction.VERIFY_EMAIL,
    }

    mock_create_user_verify_command.dto = {"user_id": "user-id", "otp": "1234"}

    mock_unit_of_work.user_repository.get.return_value = mock_user
    mock_unit_of_work.otp_repository.get.return_value = mock_otp
    mock_jwt.encode.return_value = "jwt-token"

    # Act
    response = await handler.handle(mock_create_user_verify_command)

    # Assert
    assert response.is_success is True
    assert response.message == "Create successful."
    assert response.data["token"] == "jwt-token"
    mock_jwt.encode.assert_called_once_with(
        {
            "first_name": mock_user["first_name"],
            "last_name": mock_user["last_name"],
            "email": mock_user["email"],
            "phone_number": mock_user["phone_number"],
            "user_type": UserType.DRIVER,
        }
    )


@pytest.mark.asyncio
async def test_create_user_verify_user_not_found(
    mock_unit_of_work, mock_jwt, mock_create_user_verify_command, handler
):
    # Arrange
    mock_create_user_verify_command.dto = {
        "user_id": "nonexistent-id", "otp": "1234"}

    mock_unit_of_work.user_repository.get.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_create_user_verify_command)

    assert "User with that id = nonexistent-id does not exist." in str(
        exc_info.value.errors
    )


@pytest.mark.asyncio
async def test_create_user_verify_no_otp(
    mock_unit_of_work, mock_jwt, mock_create_user_verify_command, handler
):
    # Arrange
    mock_user = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
    }

    mock_create_user_verify_command.dto = {"user_id": "user-id", "otp": "1234"}

    mock_unit_of_work.user_repository.get.return_value = mock_user
    mock_unit_of_work.otp_repository.get.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_create_user_verify_command)

    assert "Otp has not been sent to the user with id = user-id recently." in str(
        exc_info.value.errors
    )


@pytest.mark.asyncio
async def test_create_user_verify_wrong_action(
    mock_unit_of_work, mock_jwt, mock_create_user_verify_command, handler
):
    # Arrange
    mock_user = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
    }

    mock_otp = {
        "user_id": "user-id",
        "value": "1234",
        "action": OtpVerificationAction.LOGIN,  # Wrong action
    }

    mock_create_user_verify_command.dto = {"user_id": "user-id", "otp": "1234"}

    mock_unit_of_work.user_repository.get.return_value = mock_user
    mock_unit_of_work.otp_repository.get.return_value = mock_otp

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_create_user_verify_command)

    assert "Otp has not been sent to the user with id = user-id recently." in str(
        exc_info.value.errors
    )


@pytest.mark.asyncio
async def test_create_user_verify_incorrect_otp(
    mock_unit_of_work, mock_jwt, mock_create_user_verify_command, handler
):
    # Arrange
    handler = CreateUserVerifyCommandHandler(
        uow=mock_unit_of_work, jwt=mock_jwt)

    mock_user = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
    }

    mock_otp = {
        "user_id": "user-id",
        "value": "1234",
        "action": OtpVerificationAction.VERIFY_EMAIL,
    }

    mock_create_user_verify_command.dto = {
        "user_id": "user-id",
        "otp": "6543",  # Wrong OTP
    }

    mock_unit_of_work.user_repository.get.return_value = mock_user
    mock_unit_of_work.otp_repository.get.return_value = mock_otp

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_create_user_verify_command)

    assert "Otp does not match with the one sent." in str(
        exc_info.value.errors)
