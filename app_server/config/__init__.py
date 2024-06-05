#!/usr/bin/env python

import os

from sqlalchemy.engine import URL

from app_server.constants.env import Environment
from fmlib.config import FMConfig

# Find the absolute file path to the top level project directory
project_base_path = __file__.rsplit("/", 3)[0]

# Configs are loaded only once
configs = None


def _init_configs(configFile: str = "settings.toml") -> dict:
    """
    Initializes and returns a dictionary of configuration settings.

    Args:
        configFile (str, optional): The name of the configuration file. Defaults to "settings.toml".

    Returns:
        dict: A dictionary containing the configuration settings.
    """
    global configs
    if configs is None:
        configs = FMConfig(os.path.join(project_base_path, configFile)).get()
    return configs


class Config:
    """
    Base configuration class. Contains the default settings for the application.
    """

    def __init__(self) -> None:
        """
        Initializes the configuration class.
        """
        # Find the absolute file path to the top level project directory
        # project_base_path = __file__.rsplit("/", 3)[0]
        # load_dotenv(dotenv_path=os.path.join(project_base_path, ".env"))  # Load the .env file
        # SERVICE_NAME = os.environ.get("SERVICE_NAME")  # Get the service name from the .env file

        # Loading configs from toml file
        self._settings = _init_configs()

        self.SERVICE_NAME = self._settings.get("SERVICE_NAME")

        # Default settings
        self.ENV = self._settings.get("ENV", Environment.DEVELOPMENT.value)
        self.DEBUG = bool(self._settings.get("DEBUG", False))
        self.TESTING = bool(self._settings.get("TESTING", False))
        self.LOG_LEVEL = self._settings.get("LOG_LEVEL", "INFO")
        self.SECRET_KEY = self._settings.get("SECRET_KEY", "")

        # Database settings
        self.DB_HOST = self._settings.get("DB_HOST", "localhost")
        self.DB_PASSWORD = self._settings.get("DB_PASSWORD", "postgres")
        self.DB_USER = self._settings.get("DB_USER", "postgres")
        self.DB_NAME = self._settings.get("DB_NAME", "postgres")
        self.DB_PORT = int(self._settings.get("DB_PORT", 5432))
        self.DB_POOL_SIZE = int(self._settings.get("DB_POOL_SIZE", 10))

        # S3 settings
        self.S3_BUCKET_NAME = self._settings.get("S3_BUCKET_NAME", "fairmatic-data")
        self.S3_BASE_DIR = self._settings.get("S3_BASE_DIR", "fairmatic")
        self.S3_DIR_VERSION = self._settings.get("S3_DIR_VERSION", "v1")
        self.S3_REGION = self._settings.get("S3_REGION", "us-west-2")
        self.S3_TIMEOUT = int(self._settings.get("S3_TIMEOUT", 60))
        self.S3_RETRIES = int(self._settings.get("S3_RETRIES", 3))
        self.S3_MAX_CONCURRENT_REQUESTS = int(self._settings.get("S3_MAX_CONCURRENT_REQUESTS", 20))
        self.S3_ENDPOINT_URL = self._settings.get("S3_ENDPOINT_URL", "https://s3.us-west-2.amazonaws.com")
        self.S3_PRESIGNED_EXPIRY = int(self._settings.get("S3_PRESIGNED_EXPIRY", 3600))

        # Sentry settings
        self.SENTRY_DSN = self._settings.get("SENTRY_DSN", "")

        # DB DSN settings
        self.SQLALCHEMY_DATABASE_URI = URL.create(
            drivername="postgresql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

        # SuperToken settings
        self.SUPER_TOKENS_API_KEY = self._settings.get("SUPER_TOKENS_API_KEY", "")
        self.SUPER_TOKENS_CONNECTION_URI = self._settings.get("SUPER_TOKENS_CONNECTION_URI", "")
        self.API_DOMAIN = self._settings.get("API_DOMAIN", "SERVICE_NAME-service.fairamtic.com")
        self.WEBSITE_DOMAIN = self._settings.get("WEBSITE_DOMAIN", "SERVICE_NAME.fairmatic.com")
        self.CORS_ORIGIN = self._settings.get("CORS_ORIGIN", ["*"])

    def validate(self) -> None:
        """
        Validates the configuration parameters for the application.

        Raises:
            ValueError: If any configuration parameter is not of the correct type.
        """
        # Validate the configuration parameters
        if not isinstance(self.ENV, str):
            raise ValueError("ENV must be a string.")
        if not isinstance(self.DEBUG, bool):
            raise ValueError("DEBUG must be a boolean.")
        if not isinstance(self.TESTING, bool):
            raise ValueError("TESTING must be a boolean.")
        if not isinstance(self.LOG_LEVEL, str):
            raise ValueError("LOG_LEVEL must be a string.")
        if not isinstance(self.SECRET_KEY, str):
            raise ValueError("SECRET_KEY must be a string.")
        if not isinstance(self.DB_HOST, str):
            raise ValueError("DB_HOST must be a string.")
        if not isinstance(self.DB_PASSWORD, str):
            raise ValueError("DB_PASSWORD must be a string.")
        if not isinstance(self.DB_USER, str):
            raise ValueError("DB_USER must be a string.")
        if not isinstance(self.DB_NAME, str):
            raise ValueError("DB_NAME must be a string.")
        if not isinstance(self.DB_PORT, int):
            raise ValueError("DB_PORT must be a string.")
        if not isinstance(self.DB_POOL_SIZE, int):
            raise ValueError("DB_POOL_SIZE must be a string.")
        if not isinstance(self.S3_BUCKET_NAME, str):
            raise ValueError("S3_BUCKET_NAME must be a string.")
        if not isinstance(self.S3_BASE_DIR, str):
            raise ValueError("S3_BASE_DIR must be a string.")
        if not isinstance(self.S3_DIR_VERSION, str):
            raise ValueError("S3_DIR_VERSION must be a string.")
        if not isinstance(self.SENTRY_DSN, str):
            raise ValueError("SENTRY_DSN must be a string.")
        if not isinstance(self.S3_TIMEOUT, int):
            raise ValueError("S3_TIMEOUT must be an integer.")
        if not isinstance(self.S3_RETRIES, int):
            raise ValueError("S3_RETRIES must be an integer.")
        if not isinstance(self.S3_MAX_CONCURRENT_REQUESTS, int):
            raise ValueError("S3_MAX_CONCURRENT_REQUESTS must be an integer.")
        if not isinstance(self.S3_REGION, str):
            raise ValueError("S3_REGION must be a string.")
        if not isinstance(self.S3_ENDPOINT_URL, str):
            raise ValueError("S3_ENDPOINT_URL must be a string.")
        if not isinstance(self.S3_PRESIGNED_EXPIRY, int):
            raise ValueError("S3_PRESIGNED_EXPIRY must be an integer.")
        if not isinstance(self.SUPER_TOKENS_API_KEY, str):
            raise ValueError("SUPER_TOKENS_API_KEY must be a string.")
        if not isinstance(self.SUPER_TOKENS_CONNECTION_URI, str):
            raise ValueError("SUPER_TOKENS_CONNECTION_URI must be a string.")
        if not isinstance(self.API_DOMAIN, str):
            raise ValueError("API_DOMAIN must be a string.")
        if not isinstance(self.WEBSITE_DOMAIN, str):
            raise ValueError("WEBSITE_DOMAIN must be a string.")
        if not isinstance(self.CORS_ORIGIN, list):
            raise ValueError("CORS_ORIGIN must be a list.")
