from aiokafka import AIOKafkaConsumer
from albayanworker.configs.config import config
import json
import logging

logger = logging.getLogger(__name__)


async def consume_kafka_messages():
    """Consumes messages from Kafka topic and processes them."""
    # Initialize the Kafka consumer
    consumer = AIOKafkaConsumer(
        config.kafka_topic,
        bootstrap_servers=config.kafka_bootstrap_servers,
        group_id=config.kafka_group_id,
    )
    # Start the consumer
    await consumer.start()
    try:
        # Continuously listen for messages
        async for msg in consumer:
            # Read, decode, and log the message
            received_message = msg.value.decode("utf-8")
            logging.info(f"Consumed message: {received_message}")
            try:
                # Convert the message from JSON String to a dictionary
                received_payload = json.loads(received_message)
                # Process the received payload by liberoffice
            except Exception as e:
                logging.error(f"Failed to process message: {e}")

    finally:
        # Ensure the consumer is properly closed
        await consumer.stop()
