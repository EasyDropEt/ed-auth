from fastapi import APIRouter, Depends, WebSocket
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.user.dtos.some_create_dto import SomeCreateDto
from src.application.features.user.dtos.some_response_dto import SomeResponseDto
from src.application.features.user.requests.commands.some_command import SomeCommand
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/some-feature", tags=["Some Feature"])


@router.get("/get", response_model=GenericResponse[SomeResponseDto])
@rest_endpoint
async def get(mediator: Annotated[Mediator, Depends(mediator)]):
    LOG.info("Satisfying request")
    return await mediator.send(SomeCommand(dto=SomeCreateDto("Message")))


@router.post("/post", response_model=GenericResponse[SomeResponseDto])
@rest_endpoint
async def post(
    request_dto: SomeCreateDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info(f"Satisfying request {request_dto}")
    return await mediator.send(SomeCommand(dto=request_dto))


@router.websocket("/ws")
async def websocket(ws: WebSocket) -> None:
    await ws.accept()

    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Message text was: {data}")
