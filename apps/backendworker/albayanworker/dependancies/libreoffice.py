import uno
import asyncio
import logging
from albayanworker.configs.config import config
from albayanworker.utilities.libreoffice_utilites import initilize_libreoffice_sync

# Set up logging
logger = logging.getLogger(__name__)
# Global variable to hold the LibreOffice connection
libreoffice = None
# A lock to ensure thread-safe initialization
initialization_lock = asyncio.Lock()


async def get_libreoffice():
    """
    Initializes and returns a connection to a LibreOffice instance running in headless mode.
    Assumes that LibreOffice is already running and listening on the specified host and port.
    """
    # Ensure thsat global variable is used
    global libreoffice
    async with initialization_lock:
        # If already initialized, return the existing connection
        if libreoffice is not None:
            return libreoffice
        try:
            # Initialize the LibreOffice connection in a separate thread to avoid blocking
            libreoffice = await asyncio.to_thread(
                initilize_libreoffice_sync(
                    config.libreoffice_host, config.libreoffice_port
                )
            )
            logger.info("✅ Successfully connected to LibreOffice.")
            return libreoffice
        except Exception as e:
            logger.error(f"⛔️ Failed to connect to LibreOffice: {e}")
            raise
