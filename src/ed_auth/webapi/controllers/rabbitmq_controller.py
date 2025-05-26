from typing import Annotated
from uuid import UUID

from ed_domain.common.logging import get_logger
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit.schemas import RabbitQueue
from rmediator.mediator import Mediator

from ed_auth.application.features.auth.requests.commands import \
    DeleteUserCommand
from ed_auth.common.generic_helpers import get_config
from ed_auth.webapi.dependency_setup import mediator

config = get_config()
router = RabbitRouter(config["rabbitmq"]["url"])
queue = RabbitQueue(name=config["rabbitmq"]["queue"], durable=True)

LOG = get_logger()


@router.subscriber(queue)
async def delete_user(id: UUID, mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(DeleteUserCommand(id))
