import pytest
from ed_domain.common.exceptions import ApplicationException

from ed_auth.application.features.auth.handlers.commands.verify_token_command_handler import \
    VerifyTokenCommandHandler
from tests.helpers.fixture_generator import generate_fixtures

PATH = (
    "ed_auth.application.features.auth.handlers.commands.verify_token_command_handler"
)

generate_fixtures(
    (f"{PATH}.ABCUnitOfWork", "mock_unit_of_work"),
    (f"{PATH}.ABCJwtHandler", "mock_jwt"),
    (f"{PATH}.VerifyTokenCommand", "mock_verify_token_command"),
)


@pytest.fixture
def handler(
    mock_unit_of_work,
    mock_jwt,
):
    handler = VerifyTokenCommandHandler(
        uow=mock_unit_of_work,
        jwt=mock_jwt,
    )

    return handler


@pytest.mark.asyncio
async def test_valid_verify_token_command_handler(
    mock_unit_of_work,
    mock_jwt,
    mock_verify_token_command,
    handler,
):
    # Arrange
    mock_jwt.decode.return_value = {"email": "test@example.com"}
    mock_unit_of_work.auth_user_repository.get.return_value = {
        "email": "test@example.com",
        "name": "Test User",
        "logged_in": True,
    }
    mock_verify_token_command.dto = {"token": "valid_token"}

    # Act
    response = await handler.handle(mock_verify_token_command)

    # Assert
    assert response.success
    assert response.message == "Token validated."


@pytest.mark.asyncio
async def test_verify_token_command_handler_missing_email(
    mock_jwt,
    mock_verify_token_command,
    handler,
):
    # Arrange
    mock_jwt.decode.return_value = {}
    mock_verify_token_command.dto = {"token": "token_without_email"}

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_verify_token_command)

    assert exc_info.value.message == "Token validation failed."
    assert "Token is malformed." in exc_info.value.errors


@pytest.mark.asyncio
async def test_verify_token_command_handler_user_not_found(
    mock_unit_of_work,
    mock_jwt,
    mock_verify_token_command,
    handler,
):
    # Arrange
    mock_jwt.decode.return_value = {"email": "notfound@example.com"}
    mock_unit_of_work.auth_user_repository.get.return_value = None
    mock_verify_token_command.dto = {"token": "valid_token"}

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_verify_token_command)

    assert exc_info.value.message == "Token validation failed."
    assert "User not found." in exc_info.value.errors


@pytest.mark.asyncio
async def test_verify_token_command_handler_invalid_token(
    mock_jwt,
    mock_verify_token_command,
    handler,
):
    # Arrange
    mock_jwt.decode.side_effect = Exception("Invalid token")
    mock_verify_token_command.dto = {"token": "invalid_token"}

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await handler.handle(mock_verify_token_command)

    assert str(exc_info.value) == "Invalid token"
