from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
from albayanworker.dependancies.libreoffice import get_libreoffice
from albayanworker.dependancies.dyanomodb import get_dynamodb_table
from albayanworker.configs.config import config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initilizes connection with libreoffice."""
    # Connect to required databases/services
    try:
        await get_libreoffice()
        logger.info("Albayan Reports Worker successfully started.")
        yield
    except Exception as e:
        logger.error(f"Failed to connect to one or service or more {e}")
        raise  # Re-raise the exception to stop the app from starting


app = FastAPI(
    lifespan=lifespan, title="Albayan Reports Backend Worker", version="1.0.0"
)
