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

    # 1. Configuration for Connection
    # By default, use the AWS cloud settings
    dynamo_config = {
        "service_name": "dynamodb",
        "region_name": config.aws_regsion,
    }

    # 2. Local Mode Overrides
    if config.environment in ["TEST", "DEVELOPMENT"]:
        logger.info("❗️ Connecting to DynamoDB LOCAL")
        # Override the settings for DynamoDB Local
        dynamo_config["endpoint_url"] = "http://localhost:8000"
        # Dummy credentials are required for Boto3/aioboto3 to connect locally
        dynamo_config["aws_access_key_id"] = "DUMMYID"
        dynamo_config["aws_secret_access_key"] = "DUMMYSECRET"

    # 3. Create Session and Resource
    session = aioboto3.Session()

    # The 'async with' handles the lifecycle of the resource
    async with session.resource(**dynamo_config) as dynamo_resource:
        table = dynamo_resource.Table(table_name)
        return table
