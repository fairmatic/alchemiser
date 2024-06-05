from app_server.db import db
from app_server.db.error import FMEntityNotFoundException
from fmlib.db.base_model import BaseSoftDeleteModel, BaseTimestampModel, BaseUUIDPrimaryKeyModel


class BaseFMDataModel(BaseUUIDPrimaryKeyModel, BaseTimestampModel, BaseSoftDeleteModel):
    """
    Base class for FM (FileMaker) data models.
    Provides common functionality for FM data models such as retrieving entities by FM entity ID,
    soft deleting entities by FM entity ID, and validation.
    """

    __abstract__ = True

    @classmethod
    def get_for_fm_entity_id(cls, fm_entity_id: str, include_soft_deleted: bool = False):
        """
        Retrieves an entity by FM entity ID.

        Args:
            fm_entity_id (str): The FM entity ID.
            include_soft_deleted (bool, optional): Whether to include soft deleted entities. Defaults to False.

        Returns:
            The entity with the specified FM entity ID, or None if not found.
        """
        query = db.session.query(cls).filter(cls.id == fm_entity_id)
        if not include_soft_deleted:
            query = query.filter(cls.deleted.is_(False))
        entity = query.first()
        return entity

    @classmethod
    def soft_delete_fm_entity_id(cls, fm_entity_id: str) -> None:
        """
        Soft deletes an entity by FM entity ID.

        Args:
            fm_entity_id (str): The FM entity ID.

        Raises:
            FMEntityNotFoundException: If the entity with the specified FM entity ID is not found.
        """
        entity = db.session.query(cls).filter(cls.id == fm_entity_id).first()
        if entity:
            entity.soft_delete()
        else:
            raise FMEntityNotFoundException(f"FM entity {cls.__name__} not found for id {fm_entity_id}")

    def validate(self) -> None:
        """
        Validates the entity.

        This method should be overridden in derived classes to implement custom validation logic.
        """
        pass
