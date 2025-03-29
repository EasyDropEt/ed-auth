import jwt
from ed_domain.tokens.auth_payload import AuthPayload

from ed_auth.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from ed_auth.common.exception_helpers import ApplicationException, Exceptions
from ed_auth.common.logging_helpers import get_logger

LOG = get_logger()


class Jwt(ABCJwt):
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def encode(self, payload: AuthPayload) -> str:
        try:
            return jwt.encode(
                dict(payload),
                self._secret,
                algorithm=self._algorithm,
            )
        except Exception as e:
            LOG.error(f"Error encoding jwt payload: {payload}. {e}")
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Internal server error.",
                ["Internal server error."],
            )

    def decode(self, token: str) -> AuthPayload:
        try:
            return jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
            )
        except Exception as e:
            LOG.error(f"Error decoding jwt token: {token}. {e}")
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Token validation failed.",
                ["Token is malformed."],
            )
