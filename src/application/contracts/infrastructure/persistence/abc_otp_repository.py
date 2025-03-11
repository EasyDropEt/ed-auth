from abc import ABCMeta

from ed_domain_model.entities.otp import Otp

from src.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository


class ABCOtpRepository(
    ABCGenericRepository[Otp],
    metaclass=ABCMeta,
): ...
