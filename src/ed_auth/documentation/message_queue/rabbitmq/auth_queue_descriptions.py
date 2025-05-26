from ed_domain.documentation.message_queue.rabbitmq.abc_queue_descriptions import \
    ABCQueueDescriptions
from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription

from ed_auth.application.features.auth.dtos.delete_user_dto import \
    DeleteUserDto


class AuthQueueDescriptions(ABCQueueDescriptions):
    def __init__(self, connection_url: str) -> None:
        self._descriptions: list[QueueDescription] = [
            {
                "name": "delivery_job",
                "connection_url": connection_url,
                "durable": True,
                "request_model": DeleteUserDto,
            }
        ]

    @property
    def descriptions(self) -> list[QueueDescription]:
        return self._descriptions
