from ed_auth.common.logging_helpers import get_logger
from ed_auth.webapi.api import API

LOG = get_logger()


class Package:
    def __init__(self) -> None:
        self._api = API()

    def start(self) -> None:
        LOG.info("Starting Package...")
        self._api.start()

    def stop(self) -> None:
        LOG.info("Stopping Package...")
        self._api.stop()


if __name__ == "__main__":
    main = Package()

    main.start()
