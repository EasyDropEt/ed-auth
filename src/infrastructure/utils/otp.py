from random import randint

from src.application.contracts.infrastructure.utils.abc_otp import ABCOtp, OtpCode


class Otp(ABCOtp):
    def generate(self) -> OtpCode:
        return f"{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"
