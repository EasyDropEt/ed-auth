from ed_domain.common.logging import get_logger
from fastapi.middleware.cors import CORSMiddleware

from ed_auth.webapi.api import API

LOG = get_logger()


class Package:
    def __init__(self) -> None:
        self._api = API()
        self._api.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def start(self) -> None:
        LOG.info("Starting Package...")
        self._api.start()

    def stop(self) -> None:
        LOG.info("Stopping Package...")
        self._api.stop()


if __name__ == "__main__":
    main = Package()

    main.start()
