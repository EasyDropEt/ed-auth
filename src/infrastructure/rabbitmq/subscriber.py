import json

from pika import ConnectionParameters, URLParameters, spec
from pika.adapters import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from src.application.contracts.infrastructure.message_queue.abc_subscriber import (
    ABCSubscriber,
    CallbackFunction,
)
from src.common.logging_helpers import get_logger
from src.common.typing.config import TestMessage

LOG = get_logger()


class RabbitMQSubscriber(ABCSubscriber[TestMessage]):
    def __init__(
        self,
        queue: str,
        callback_function: CallbackFunction,
    ) -> None:
        self._queue = queue
        self._callback_function = callback_function
        self._connection = self._connect_with_url_parameters("url")

    def start(self) -> None:
        LOG.info("Starting subscriber...")
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)

        self._channel.basic_consume(
            queue=self._queue, on_message_callback=self._callback, auto_ack=True
        )
        self._channel.start_consuming()

    def stop(self) -> None:
        LOG.info("Stopping subscriber")
        self._connection.close()

    def _connect_with_connection_parameters(
        self, host: str, port: int
    ) -> BlockingConnection:
        connection_parameters = ConnectionParameters(host, port)
        return BlockingConnection(connection_parameters)

    def _connect_with_url_parameters(self, url: str) -> BlockingConnection:
        connection_parameters = URLParameters(url)
        return BlockingConnection(connection_parameters)

    def _callback(
        self,
        channel: BlockingChannel,
        method: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes,
    ) -> None:
        try:
            message: TestMessage = json.loads(body.decode("utf-8"))

            self._callback_function(message)

        except json.JSONDecodeError as e:
            LOG.error(f"Failed to decode message: {e}")

        except KeyError as e:
            LOG.error(f"Missing key in message: {e}")


def example_callback(message: TestMessage) -> None:
    LOG.info(f" [x] Received '{message}'")
