# S3 utility functions

import boto3
from botocore.client import Config


# Create an S3 client
_S3 = None


def _initialize_s3(region_name: str, endpoint_url: str, timeout: int = 30, retries: int = 3, max_pool_connections: int = 25) -> boto3.client:
    """
    Initialize the S3 client for the application.
    """
    try:
        # Create the S3 configuration
        s3_config = Config(
            connect_timeout=timeout,
            retries=retries,
            max_pool_connections=max_pool_connections,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )

        # Create the S3 client
        s3 = boto3.client("s3", config=s3_config)
        return s3
    except Exception as e:
        # Raise an exception
        raise SystemError(f"Error initializing S3 client: {str(e)}")

def init_s3(region_name: str, endpoint_url: str, timeout: int = 30, retries: int = 3, max_pool_connections: int = 25) -> None:
    """
    Initialize the S3 client for the application.

    Args:
        region_name (str): The name of the AWS region where the S3 bucket is located.
        endpoint_url (str): The URL of the S3 service endpoint.
        timeout (int, optional): The maximum amount of time (in seconds) to wait for a response from the S3 service. Defaults to 30 seconds.
        retries (int, optional): The maximum number of times to retry a request to the S3 service. Defaults to 3 retries.
        max_pool_connections (int, optional): The maximum number of connections to pool for reuse when making requests to the S3 service. Defaults to 25 connections.

    Returns:
        None
    
    Example Usage:
        # Initialize the S3 client
        init_s3(region_name="us-east-1", endpoint_url="https://s3.us-east-1.amazonaws.com")
    """

    global _S3
    if _S3 is None:
        _S3 = _initialize_s3(region_name, endpoint_url, timeout, retries, max_pool_connections)

def get_s3_client() -> boto3.client:
    """
    Returns an instance of the `boto3.client` class to interact with the Amazon S3 service.

    Args:
        None
    Returns:
        boto3.client: An instance of the `boto3.client` class that can be used to interact with the Amazon S3 service.
    
    """
    global _S3
    if _S3 is None:
        raise SystemError("S3 client has not been initialized")
    return _S3


def get_s3_bucket(bucket_name: str) -> boto3.resource:
    """
    Get an S3 bucket for the application.

    Args:
        bucket_name (str): The name of the bucket to get.

    Returns:
        boto3.resource: The S3 bucket for the application.
    """
    # Get the S3 resource
    s3_resource = get_s3_client()

    # Get the bucket
    bucket = s3_resource.Bucket(bucket_name)
    return bucket


def get_s3_object(bucket_name: str, key: str) -> boto3.resource:
    """
    Get an S3 object for the application.

    Args:
        bucket_name (str): The name of the bucket to get.
        key (str): The key of the object to get.

    Returns:
        boto3.resource: The S3 object for the application.
    """
    # Get the S3 resource
    s3_resource = get_s3_client()

    # Get the object
    obj = s3_resource.Object(bucket_name, key)
    return obj


def get_s3_object_url(bucket_name: str, key: str, presigned_expiry: int) -> str:
    """
    Get a pre-signed URL for an object in an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        key (str): The key of the object in the S3 bucket.
        presigned_expiry (int): The expiry time in seconds for the generated pre-signed URL.

    Returns:
        str: The generated pre-signed URL for the specified object in the specified bucket.
    """
    s3_client = get_s3_client()  # Get the S3 client
    obj_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=presigned_expiry,
    )  # Generate the pre-signed URL
    return obj_url
