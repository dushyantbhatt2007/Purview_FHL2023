import json
from pyapacheatlas.core import PurviewClient, AtlasEntity, AtlasProcess, EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.core.util import GuidTracker


class EntityLineage:
    def __init__(self, client: PurviewClient):
        self.client = client

    def create_or_update_lineage(self, lineage_json, gt: GuidTracker):
        procType = EntityTypeDef(
            "ProcessWithColumnMapping",
            superTypes=["Process"],
            attributeDefs=[
                AtlasAttributeDef("columnMapping")
            ]
        )

        # Upload the type definition
        type_results = self.client.upload_typedefs(entityDefs=[procType], force_update=True)
        print(json.dumps(type_results, indent=2))

        source_entity = AtlasEntity(
            name=lineage_json["sourceEntity"]["name"],
            typeName=lineage_json["sourceEntity"]["typeName"],
            qualified_name=lineage_json["sourceEntity"]["qualifiedName"],
            guid=gt.get_guid()
        )
        target_entity = AtlasEntity(
            name=lineage_json["targetEntity"]["name"],
            typeName=lineage_json["targetEntity"]["typeName"],
            qualified_name=lineage_json["targetEntity"]["qualifiedName"],
            guid=gt.get_guid()
        )
        column_mappings = lineage_json["columnMappings"]

        # The Atlas Process is the lineage component that links the two
        # entities together. The inputs and outputs need to be the "header"
        # version of the atlas entities, so specify minimum = True to
        # return just guid, qualifiedName, and typeName.
        process = AtlasProcess(
            name=lineage_json["process"]["name"],
            typeName=lineage_json["process"]["typeName"],
            qualified_name=lineage_json["process"]["typeName"],
            inputs=[source_entity],
            outputs=[target_entity],
            guid=gt.get_guid(),
            attributes={"columnMapping": json.dumps(column_mappings)}
        )

        results = self.client.upload_entities(
            batch=[source_entity, target_entity, process]
        )
        return results
