import aioboto3
import logging
from albayanworker.configs.config import config

# Set up logging
logger = logging.getLogger(__name__)

# Single session and persistent resource for the application lifetime
session = aioboto3.Session()
_dynamo_resource = None
_tables_cache = {}


async def get_dynamodb_resource():
    """Initialize and return the persistent aioboto3 DynamoDB resource."""
    global _dynamo_resource
    if _dynamo_resource is None:
        # Enter the async context and keep the resource alive for the app lifetime
        _dynamo_resource = await session.resource(
            "dynamodb",
            region_name=config.aws_region,
            endpoint_url=config.dynamodb_endpoint,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
        ).__aenter__()
    return _dynamo_resource


async def close_dynamodb_resource():
    """Close the persistent aioboto3 resource and clear cached tables."""
    global _dynamo_resource, _tables_cache
    if _dynamo_resource is not None:
        await _dynamo_resource.__aexit__(None, None, None)
        _dynamo_resource = None
        _tables_cache.clear()


async def get_dynamodb_table(table_name: str):
    """
    Returns a boto3 DynamoDB Table resource, initializing the aioboto3 resource
    and caching table objects for reuse across the application lifetime.
    """
    resource = await get_dynamodb_resource()
    if table_name not in _tables_cache:
        # Table() is an awaitable and must be awaited
        _tables_cache[table_name] = await resource.Table(table_name)
    return _tables_cache[table_name]
