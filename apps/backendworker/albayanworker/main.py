from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
from albayanworker.dependancies.libreoffice import get_libreoffice
from albayanworker.dependancies.dyanomodb import get_dynamodb_table
from albayanworker.dependancies.dyanomodb import close_dynamodb_resource
from albayanworker.configs.config import config
from albayanworker.routes.report_creation_router import report_creation_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initilizes connection with libreoffice and check if dynamodb tables exists and folders exits."""
    # Connect to required databases/services
    try:
        await get_libreoffice()
        await get_dynamodb_table(config.definition_table)
        await get_dynamodb_table(config.processing_table)
        config.create_directories_if_not_exists()
        logger.info("Albayan Reports Worker successfully started.")
        yield
    except Exception as e:
        logger.error(f"Failed to connect to one or service or more {e}")
        raise
    finally:
        # Clean up aioboto3 resources opened during startup
        await close_dynamodb_resource()


app = FastAPI(
    lifespan=lifespan, title="Albayan Reports Backend Worker", version="1.0.0"
)

app.include_router(report_creation_router)
