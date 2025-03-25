import pytest

from ed_auth.application.features.auth.handlers.commands.create_user_command_handler import \
    CreateUserCommandHandler
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.handlers.commands.create_user_command_handler"


generate_fixtures(
    (f"{PATH}.ABCUnitOfWork", "mock_unit_of_work"),
    (f"{PATH}.ABCOtp", "mock_otp"),
    (f"{PATH}.ABCPassword", "mock_password"),
    (f"{PATH}.CreateUserCommand", "mock_create_user_command"),
    (f"{PATH}.CreateUserDtoValidator", "mock_create_user_dto_validator"),
)


@pytest.mark.asyncio
async def test_create_user_success(
    mock_unit_of_work, mock_otp, mock_password, mock_create_user_command
):
    # Arrange
    handler = CreateUserCommandHandler(
        uow=mock_unit_of_work, otp=mock_otp, password=mock_password
    )

    mock_create_user_command.dto = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "password": "securepassword",
    }
    mock_password.hash.return_value = "hashedpassword"
    mock_otp.generate.return_value = "123456"

    mock_unit_of_work.user_repository.create.return_value = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "password": "hashedpassword",
        "verified": False,
        "create_datetime": "2025-03-25T00:00:00Z",
        "update_datetime": "2025-03-25T00:00:00Z",
    }

    # Act
    response = await handler.handle(mock_create_user_command)

    # Assert
    print(response.to_dict())
    assert response.is_success is True
    assert response.message == "Otp sent successfully."
    assert response.data is not None
    assert response.data["first_name"] == "John"
    assert response.data["last_name"] == "Doe"

    mock_unit_of_work.user_repository.create.assert_called_once()
    mock_unit_of_work.otp_repository.create.assert_called_once()
    mock_password.hash.assert_called_once_with("securepassword")
    mock_otp.generate.assert_called_once()
