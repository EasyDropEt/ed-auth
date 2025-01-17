import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.common.exception_helpers import ApplicationException
from src.common.logging_helpers import get_logger
from src.common.singleton_helpers import SingletonMeta
from src.webapi.common.helpers import GenericResponse
from src.webapi.controllers import auth_controller

LOG = get_logger()


class API(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._app = FastAPI()

    @property
    def app(self):
        return self._app

    def start(self) -> None:
        LOG.info("Starting api...")
        self._include_routers()
        self._contain_exceptions()

        uvicorn.run(self._app, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        LOG.info("API does not need to be stopped...")

    def _include_routers(self) -> None:
        LOG.info("Including routers...")
        self._app.include_router(auth_controller.ROUTER)

    def _contain_exceptions(self) -> None:
        @self._app.exception_handler(ApplicationException)
        async def application_exception_handler(
            request: Request, exception: ApplicationException
        ) -> JSONResponse:
            return JSONResponse(
                status_code=exception.error_code,
                content=GenericResponse(
                    is_success=False,
                    message=exception.message,
                    errors=exception.errors,
                    data=None,
                ).to_dict(),
            )
