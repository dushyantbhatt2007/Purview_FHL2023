from pyapacheatlas.core.util import GuidTracker

from entity_operations.entity import Entity
from lineage.entity_lineage import EntityLineage
from utils.metadata import get_all_entities_path, load_json
from utils.purview_client import with_purview_client


@with_purview_client
def update_entities(client):
    gt = GuidTracker()
    entity = Entity(client=client)
    file_paths = get_all_entities_path("_entity.json")
    for file_path in file_paths:
        columns = []
        entity_json = load_json(file_path=file_path)
        entity_to_be_created = entity.as_atlas_entity(entity_json=entity_json["entity"], gt=gt)
        for column_json in entity_json["columns"]:
            columns.append(entity.as_atlas_entity_column(column_json=column_json, gt=gt))
        entity.create_or_update_entity(entity=entity_to_be_created, columns=columns)


@with_purview_client
def update_entity_lineage(client):
    gt = GuidTracker()
    entity_lineage = EntityLineage(client=client)
    file_paths = get_all_entities_path("_lineage.json")
    for file_path in file_paths:
        entity_lineage_json = load_json(file_path=file_path)
        entity_lineage.create_or_update_lineage(lineage_json=entity_lineage_json, gt=gt)


if __name__ == '__main__':
    update_entities()
    update_entity_lineage()
