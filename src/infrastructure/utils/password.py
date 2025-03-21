import jwt
from ed_domain_model.tokens.auth_payload import AuthPayload
from passlib.context import CryptContext

from src.application.contracts.infrastructure.utils.abc_password import \
    ABCPassword


class Password(ABCPassword):
    def __init__(self, scheme: str) -> None:
        self._context = CryptContext(schemes=[scheme], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        return self._context.verify(password, hash)
