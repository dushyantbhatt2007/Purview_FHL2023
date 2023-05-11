import json
from pyapacheatlas.core import AtlasEntity, PurviewClient


class Entity:
    def __init__(self, client: PurviewClient):
        self.client = client

    @staticmethod
    def as_atlas_entity(json, guid) -> AtlasEntity:
        return AtlasEntity(
            name=json['attributes']['name'],
            typeName=json['typeName'],
            qualified_name=json['attributes']['qualifiedName'],
            description=json['attributes']['userDescription'],
            guid=guid
        )

    @staticmethod
    def as_atlas_entity_column(json, guid) -> AtlasEntity:
        return AtlasEntity(
            name=json["attributes"]["name"],
            typeName=json["typeName"],
            qualified_name=json["attributes"]["qualifiedName"],
            attributes=json["attributes"],
            guid=guid
        )

    def create_or_update_entity(self, entity: AtlasEntity, columns: [AtlasEntity]):
        batch = [entity]
        for column in columns:
            column.addRelationship(table=entity)
            batch.append(column)

        upload_results = self.client.upload_entities(
            batch=batch
        )

        print(upload_results)

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



