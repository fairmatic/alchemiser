import uuid
from datetime import datetime
from typing import Dict

from sqlalchemy import Column, DateTime, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class BaseSoftDeleteModel(Base):
    """
    An abstract class that provides functionality for soft deleting database records.
    Soft deleting means marking a record as deleted without actually removing it from the database.
    """

    __abstract__ = True

    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime)

    def soft_delete(self) -> None:
        """
        Marks the record as deleted by setting the `deleted` field to `True` and updating the `deleted_at` field with the current datetime.
        """
        self.deleted = True
        self.deleted_at = datetime.utcnow()


class BaseTimestampModel(Base):
    """
    Abstract base class that provides timestamp functionality to its subclasses.
    """

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BaseUserCreatedModel(Base):
    """
    Abstract base class that provides timestamp functionality to its subclasses.

    Attributes:
        created_by (UUID): The ID of the user who created the model instance.

    Methods:
        __repr__(): Returns a string representation of the model instance.
    """

    __abstract__ = True

    created_by = Column(UUID(as_uuid=True), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, created_at={self.created_at})"


class BaseUserUpdatedModel(Base):
    """
    An abstract base class that represents a model with an additional field 'updated_by' that stores the UUID of the user who last updated the model.
    """

    __abstract__ = True

    updated_by = Column(UUID(as_uuid=True), nullable=True)

    def set_updated_by(self, updated_by: str) -> None:
        """
        Sets the value of the 'updated_by' field to the provided UUID.

        Args:
            updated_by: The UUID of the user who last updated the model.
        """
        self.updated_by = updated_by


class BaseUserDeletedModel(BaseSoftDeleteModel):
    """
    Base class for models that support soft deletion with a reference to the user who deleted it.
    """

    __abstract__ = True

    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    def set_deleted(self, deleted_by) -> None:
        """
        Set the deleted_by attribute and perform soft deletion.
        :param deleted_by: The user who deleted the model.
        """
        self.deleted_by = deleted_by
        self.soft_delete()


class BaseUUIDPrimaryKeyModel(Base):
    """
    Base model class with UUID primary key.

    Attributes:
        id (UUID): The UUID primary key column.
    """

    __abstract__ = True
    id = Column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, primary_key=True
    )  # TODO: Explore and Use TypeID with UUID7 instead of UUID4

    def to_dict(self) -> Dict:
        """
        Convert the object to a dictionary representation.

        Returns:
            dict: The dictionary representation of the object.
        """
        mapper = object_mapper(self)

        # Initialize an empty dictionary
        data = {}

        # Iterate over the object's attributes
        for column in mapper.columns:
            # Get the attribute name and value
            attr_name = column.name
            attr_value = getattr(self, attr_name)

            # Add the attribute to the dictionary
            data[attr_name] = attr_value

        return data