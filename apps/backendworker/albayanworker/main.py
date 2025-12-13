from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
from albayanworker.dependancies.libreoffice import get_libreoffice
from albayanworker.dependancies.dyanomodb import get_dynamodb_table
from albayanworker.dependancies.kafaka_consumer import consume_kafka_messages
from albayanworker.configs.config import config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initilizes connection with DynamoDB, libreoffice and kafka."""
    # Connect to required databases/services
    try:
        await get_libreoffice()
        await get_dynamodb_table(config.definition_table)
        await get_dynamodb_table(config.processing_table)
        await consume_kafka_messages()
        logger.info("Albayan Reports Worker successfully started.")
        yield
    except Exception as e:
        logger.error(f"Failed to connect to one or service or more {e}")
        raise  # Re-raise the exception to stop the app from starting


app = FastAPI(
    lifespan=lifespan, title="Albayan Reports Backend Worker", version="1.0.0"
)
