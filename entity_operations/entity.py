import json
from pyapacheatlas.core import AtlasEntity, PurviewClient
from pyapacheatlas.core.util import GuidTracker


class Entity:
    def __init__(self, client: PurviewClient):
        self.client = client

    @staticmethod
    def as_atlas_entity(entity_json, gt:GuidTracker) -> AtlasEntity:
        return AtlasEntity(
            name=entity_json['attributes']['name'],
            typeName=entity_json['typeName'],
            qualified_name=entity_json['qualifiedName'],
            description=entity_json['attributes']['userDescription'],
            guid=gt.get_guid()
        )

    @staticmethod
    def as_atlas_entity_column(column_json, gt:GuidTracker) -> AtlasEntity:
        return AtlasEntity(
            name=column_json["attributes"]["name"],
            typeName=column_json["typeName"],
            qualified_name=column_json["qualifiedName"],
            attributes=column_json["attributes"],
            guid=gt.get_guid()
        )

    def create_or_update_entity(self, entity: AtlasEntity, columns: [AtlasEntity]):
        batch = [entity]
        for column in columns:
            column.addRelationship(table=entity)
            batch.append(column)

        upload_results = self.client.upload_entities(
            batch=batch
        )
        return upload_results

    def get_entity_by_guid(self, guid: str) -> None:
        if not guid:
            raise ValueError("Qualified name is required.")

        entities = self.client.get_entity(
            guid=guid
        )

        if not len(entities) > 0:
            print(f"No entity_operations found with qualified name: {guid}")
            return

        print(entities["entities"][0])
        return AtlasEntity.from_json(entities["entities"][0])

    def get_entity_by_qualified_name(self, qualified_name: str, type_name: str) -> None:
        """
        Gets the entity_operations from Purview with the specified qualified name and type name.

        Args:
            client: The PurviewClient object representing the Purview client.
            qualified_name: The qualified name of the entity_operations to retrieve.

        Raises:
            ValueError: If the qualified name is not provided.
        """
        if not qualified_name:
            raise ValueError("Qualified name is required.")

        entities = self.client.get_entity(
            qualifiedName=[qualified_name],
            typeName=type_name
        )

        if not len(entities) > 0:
            print(f"No entity_operations found with qualified name: {qualified_name}")
            return

        print(entities["entities"][0])
        return AtlasEntity.from_json(entities["entities"][0])
