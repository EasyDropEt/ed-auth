import pytest
from ed_domain.common.exceptions import ApplicationException

from ed_auth.application.features.auth.handlers.commands.create_user_command_handler import \
    CreateUserCommandHandler
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.handlers.commands.create_user_command_handler"


generate_fixtures(
    (f"{PATH}.ABCApi", "mock_api"),
    (f"{PATH}.ABCUnitOfWork", "mock_unit_of_work"),
    (f"{PATH}.ABCOtpGenerator", "mock_otp"),
    (f"{PATH}.ABCPasswordHandler", "mock_password"),
    (f"{PATH}.CreateUserCommand", "mock_create_user_command"),
    (f"{PATH}.CreateUserDtoValidator", "mock_create_user_dto_validator"),
)


@pytest.fixture
def handler(
    mock_api,
    mock_unit_of_work,
    mock_otp,
    mock_password,
    mock_create_user_dto_validator,
):
    handler = CreateUserCommandHandler(
        api=mock_api, uow=mock_unit_of_work, otp=mock_otp, password=mock_password
    )
    handler._dto_validator = mock_create_user_dto_validator

    return handler


@pytest.mark.asyncio
async def test_create_user_success(
    mock_unit_of_work,
    mock_otp,
    mock_password,
    mock_create_user_command,
    mock_create_user_dto_validator,
    handler,
):
    # Arrange
    mock_create_user_command.dto = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "password": "SecurePassw0rd!",
    }
    mock_password.hash.return_value = "hashedpassword"
    mock_otp.generate.return_value = "123456"
    mock_create_user_dto_validator.validate.return_value.is_valid = True

    mock_unit_of_work.auth_user_repository.create.return_value = {
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
    assert response.is_success is True
    assert response.message == "User created successfully. Verify email."
    assert response.data is not None
    assert response.data["first_name"] == "John"
    assert response.data["last_name"] == "Doe"

    mock_unit_of_work.auth_user_repository.create.assert_called_once()
    mock_unit_of_work.otp_repository.create.assert_called_once()
    mock_password.hash.assert_called_once_with("SecurePassw0rd!")
    mock_otp.generate.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["dto", "errors"],
    [
        (
            {
                "first_name": "",
                "last_name": "Doe",
            },
            ["First name is required", "Either email or phone number must be provided"],
        ),
        (
            {
                "first_name": "John",
                "last_name": "",
            },
            ["Last name is required", "Either email or phone number must be provided"],
        ),
        (
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "",
                "phone_number": "",
            },
            ["Either email or phone number must be provided"],
        ),
    ],
)
async def test_create_user_validation_failure(
    dto,
    errors,
    mock_unit_of_work,
    mock_otp,
    mock_password,
    mock_create_user_command,
    mock_create_user_dto_validator,
    handler,
):
    # Arrange
    mock_create_user_command.dto = dto

    mock_create_user_dto_validator.validate.return_value.is_valid = False
    mock_create_user_dto_validator.validate.return_value.errors = errors

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_create_user_command)

    print(exc_info.value.errors)
    assert "Creating account failed." == exc_info.value.message
    assert all(error in exc_info.value.errors for error in errors)
    mock_unit_of_work.auth_user_repository.create.assert_not_called()
    mock_unit_of_work.otp_repository.create.assert_not_called()
    mock_password.hash.assert_not_called()
    mock_otp.generate.assert_not_called()
