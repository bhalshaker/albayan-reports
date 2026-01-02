from pydantic import BaseModel
from enum import Enum


class ProcessingStatus(Enum):
    """
    An enumeration of processing statuses.
    """

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
