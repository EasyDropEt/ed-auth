from uuid import UUID

from ed_domain.services.common.api_response import ApiResponse

from ed_auth.application.features.auth.dtos import (CreateUserDto,
                                                    CreateUserVerifyDto,
                                                    LoginUserDto,
                                                    LoginUserVerifyDto,
                                                    UnverifiedUserDto, UserDto,
                                                    VerifyTokenDto)
from ed_auth.common.api_helpers import ApiClient
from ed_auth.documentation.abc_auth_api_client import ABCAuthApiClient
from ed_auth.documentation.endpoints import AuthEndpoint


class AuthApiClient(ABCAuthApiClient):
    def __init__(self, auth_api: str) -> None:
        self._driver_endpoints = AuthEndpoint(auth_api)

    def create_get_otp(
        self, create_user_dto: CreateUserDto
    ) -> ApiResponse[UnverifiedUserDto]:
        endpoint = self._driver_endpoints.get_description("create_get_otp")

        api_client = ApiClient[UnverifiedUserDto](endpoint)

        return api_client({"request": create_user_dto})

    def create_verify_otp(
        self, create_user_verify_dto: CreateUserVerifyDto
    ) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("create_verify_otp")

        api_client = ApiClient[UserDto](endpoint)
        return api_client({"request": create_user_verify_dto})

    def login_get_otp(
        self, login_user_dto: LoginUserDto
    ) -> ApiResponse[UnverifiedUserDto]:
        endpoint = self._driver_endpoints.get_description("login_get_otp")

        api_client = ApiClient[UnverifiedUserDto](endpoint)

        return api_client({"request": login_user_dto})

    def login_verify_otp(
        self, login_user_verify_dto: LoginUserVerifyDto
    ) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("login_verify_otp")

        api_client = ApiClient[UserDto](endpoint)

        return api_client({"request": login_user_verify_dto})

    def verify_token(self, verify_token_dto: VerifyTokenDto) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("verify_token")

        api_client = ApiClient[UserDto](endpoint)

        return api_client({"request": verify_token_dto})

    def delete_user(self, id: UUID) -> ApiResponse[None]:
        endpoint = self._driver_endpoints.get_description("delete_user")

        api_client = ApiClient[None](endpoint)

        return api_client({"path_params": {"user_id": str(id)}})
