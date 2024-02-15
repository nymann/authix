import logging

from confluent_kafka import KafkaError
from confluent_kafka import Message
from confluent_kafka import Producer

from authix.core.config import RevocationConfig
from authix.domain.revocation.event import RevocationEvent
from authix.domain.revocation.publisher import RevocationPublisher


class RevocationKafkaPublisher(RevocationPublisher):
    def __init__(self, config: RevocationConfig) -> None:
        self._producer = Producer({"bootstrap.servers": config.bootstrap_servers()})
        self._topic = config.kafka_topic

    async def publish(self, revocation_event: RevocationEvent) -> None:
        logging.debug("sending kafka event")
        self._producer.poll(0)
        self._producer.produce(
            topic=self._topic,
            key=revocation_event.message_key(),
            value=revocation_event.model_dump_json().encode(),
            on_delivery=self._on_delivery,
        )

    def _on_delivery(self, error: KafkaError, message: Message) -> None:
        if error:
            logging.error("Failed to publish message to '%s'.", self._topic)
        else:
            logging.debug("Published '%s' successfully to '%s'", message.key(), self._topic)
