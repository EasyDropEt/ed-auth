from abc import ABCMeta, abstractmethod
from typing import Annotated

OtpCode = Annotated[str, "A 4 number code"]


class ABCOtp(metaclass=ABCMeta):
    @abstractmethod
    def generate(self) -> OtpCode: ...
