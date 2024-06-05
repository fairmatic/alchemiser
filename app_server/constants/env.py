"""
This module contains a collection of constants used throughout the application.
"""
# Environment variables
from enum import Enum


class Environment(Enum):
    """
    Enum class representing the different environments of the application.
    """

    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    STAGE = "stage"
    TEST = "test"
