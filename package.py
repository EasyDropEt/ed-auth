from threading import Thread

from src.common.logging_helpers import get_logger
from src.infrastructure.rabbitmq.producer import RabbitMQProducer
from src.infrastructure.rabbitmq.subscriber import RabbitMQSubscriber, example_callback
from src.webapi.api import API

LOG = get_logger()


class Package:
    def __init__(self) -> None:
        self._rabbitmq_producer = RabbitMQProducer("test_queue")
        self._rabbitmq_subscriber = RabbitMQSubscriber("test_queue", example_callback)
        self._api = API()

    def start_producer(self) -> None:
        self._rabbitmq_producer.start()

        self._rabbitmq_producer.publish({"title": "Hello, world!"})

    def start_subscriber(self) -> None:
        self._rabbitmq_subscriber.start()

    def start_api(self) -> None:
        self._api.start()

    def stop(self) -> None:
        self._api.stop()
        self._rabbitmq_producer.stop()
        self._rabbitmq_subscriber.stop()


if __name__ == "__main__":
    main = Package()

    subscriber_thread = Thread(target=main.start_subscriber, daemon=False)
    producer_thread = Thread(target=main.start_producer, daemon=False)

    subscriber_thread.start()
    producer_thread.start()
    main.start_api()
