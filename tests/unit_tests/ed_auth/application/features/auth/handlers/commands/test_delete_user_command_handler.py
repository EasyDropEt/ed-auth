import pytest
from ed_domain.common.exceptions import ApplicationException

from ed_auth.application.features.auth.handlers.commands.delete_user_command_handler import \
    DeleteUserCommandHandler
from tests.helpers.fixture_generator import generate_fixtures

PATH = "ed_auth.application.features.auth.handlers.commands.delete_user_command_handler"

generate_fixtures(
    (f"{PATH}.ABCAsyncUnitOfWork", "mock_unit_of_work"),
    (f"{PATH}.DeleteUserCommand", "mock_delete_user_command"),
)


@pytest.mark.asyncio
async def test_delete_user_success(mock_unit_of_work, mock_delete_user_command):
    # Arrange
    handler = DeleteUserCommandHandler(uow=mock_unit_of_work)
    mock_delete_user_command.id = "user-id"

    mock_unit_of_work.auth_user_repository.get.return_value = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
    }
    mock_unit_of_work.auth_user_repository.delete.return_value = True

    # Act
    response = await handler.handle(mock_delete_user_command)

    # Assert
    assert response.is_success is True
    assert response.message == "User deleted successfully."
    assert response.data is None
    mock_unit_of_work.auth_user_repository.get.assert_called_once_with(
        id="user-id")
    mock_unit_of_work.auth_user_repository.delete.assert_called_once_with(
        "user-id")


@pytest.mark.asyncio
async def test_delete_user_not_found(mock_unit_of_work, mock_delete_user_command):
    # Arrange
    handler = DeleteUserCommandHandler(uow=mock_unit_of_work)
    mock_delete_user_command.id = "nonexistent-id"

    mock_unit_of_work.auth_user_repository.get.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_delete_user_command)

    assert "User not found." in str(exc_info.value.errors)
    mock_unit_of_work.auth_user_repository.get.assert_called_once_with(
        id="nonexistent-id"
    )
    mock_unit_of_work.auth_user_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_delete_user_internal_error(mock_unit_of_work, mock_delete_user_command):
    # Arrange
    handler = DeleteUserCommandHandler(uow=mock_unit_of_work)
    mock_delete_user_command.id = "user-id"

    mock_unit_of_work.auth_user_repository.get.return_value = {
        "id": "user-id",
        "first_name": "John",
        "last_name": "Doe",
    }
    mock_unit_of_work.auth_user_repository.delete.return_value = False

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await handler.handle(mock_delete_user_command)

    assert "Internal server error." in str(exc_info.value.errors)
    mock_unit_of_work.auth_user_repository.get.assert_called_once_with(
        id="user-id")
    mock_unit_of_work.auth_user_repository.delete.assert_called_once_with(
        "user-id")
