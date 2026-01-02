import aioboto3
import logging
from albayanworker.configs.config import config

# Set up logging
logger = logging.getLogger(__name__)
# Global variable to hold the LibreOffice co


async def get_dynamodb_table(table_name: str):
    """
    Dependency function that initializes and yields the aioboto3 DynamoDB Table resource.
    """

    # Configuration for Connection
    dynamo_config = {
        "service_name": "dynamodb",
        "region_name": config.aws_region,
        "endpoint_url": config.dynamodb_endpoint,
        "aws_access_key_id": config.aws_access_key_id,
        "aws_secret_access_key": config.aws_secret_access_key,
    }

    # Create Session and Resource
    session = aioboto3.Session()

    # The 'async with' handles the lifecycle of the resource
    async with session.resource(**dynamo_config) as dynamo_resource:
        table = dynamo_resource.Table(table_name)
        return table
