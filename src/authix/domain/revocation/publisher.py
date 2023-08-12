import logging

from confluent_kafka import KafkaError
from confluent_kafka import Message
from confluent_kafka import Producer

from authix.core.config import RevocationConfig
from authix.domain.revocation.event import RevocationEvent


class RevocationPublisher:
    def __init__(self, config: RevocationConfig) -> None:
        self._producer = Producer({"bootstrap.servers": config.bootstrap_servers()})
        self._topic = config.kafka_topic

    async def publish_and_forget(self, revocation_event: RevocationEvent) -> None:
        try:
            await self.publish(revocation_event=revocation_event)
        except Exception as e:
            logging.error(f"Failed to publish revocation event {revocation_event}", e)

    async def publish(self, revocation_event: RevocationEvent) -> None:
        logging.info("sending kafka event")
        self._producer.poll(0)
        self._producer.produce(
            topic=self._topic,
            key=revocation_event.message_key(),
            value=revocation_event.model_dump_json().encode(),
            on_delivery=self._on_delivery,
        )

    def _on_delivery(self, error: KafkaError, message: Message) -> None:
        if error:
            logging.error("Failed to publish.")
        else:
            logging.debug("Published %s successfully", message.key())
