from enum import Enum
from dataclasses import dataclass

class Role(Enum):
    """
    Class representing user roles.
    """

    ADMIN = "admin"
    USER = "user"


@dataclass
class Permission(Enum):
    """
    Class representing permission levels.
    """

    WRITE = "w"
    READ = "r"
    UPDATE = "u"
    DELETE = "d"
  