from ed_infrastructure.documentation.message_queue.rabbitmq.rabbitmq_producer import \
    RabbitMQProducer

from ed_auth.application.features.auth.dtos import DeleteUserDto
from ed_auth.documentation.message_queue.rabbitmq.abc_auth_rabbitmq_subscriber import \
    ABCAuthRabbitMQSubscriber
from ed_auth.documentation.message_queue.rabbitmq.auth_queue_descriptions import \
    AuthQueueDescriptions


class AuthRabbitMQSubscriber(ABCAuthRabbitMQSubscriber):
    def __init__(self, connection_url: str) -> None:
        self._connection_url = connection_url
        self._queues = AuthQueueDescriptions(connection_url)

    def delete_user(self, delete_user_dto: DeleteUserDto) -> None:
        queue = self._queues.get_queue("create_delivery_job")
        producer = RabbitMQProducer[DeleteUserDto](
            queue["connection_url"], queue["name"]
        )
        producer.start()
        producer.publish(delete_user_dto)
        producer.stop()
