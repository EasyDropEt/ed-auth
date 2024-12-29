from src.common.logging_helpers import get_logger
from src.webapi.api import API

LOG = get_logger()


class Package:
    def __init__(self) -> None:
        self._api = API()

    def start_api(self) -> None:
        self._api.start()

    def stop(self) -> None:
        self._api.stop()


if __name__ == "__main__":
    main = Package()

    main.start_api()
