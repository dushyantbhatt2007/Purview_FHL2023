from pyapacheatlas.core.util import GuidTracker
from pyapacheatlas.core import PurviewClient

from entity_operations.entity import Entity
from utils.metadata import get_all_entities_path, get_entity_json
from utils.purview_client import with_purview_client


@with_purview_client
def run(client):
    gt = GuidTracker()
    entity = Entity(client=client)
    file_paths = get_all_entities_path("")
    for file_path in file_paths:
        columns = []
        entity_json = get_entity_json(file_path=file_path)
        entity_to_be_created = entity.as_atlas_entity(json=entity_json["entity"], guid=gt.get_guid())
        for column_json in entity_json["columns"]:
            columns.append(entity.as_atlas_entity_column(column_json, gt.get_guid()))
        entity.create_or_update_entity(entity=entity_to_be_created, columns=columns)





if __name__ == '__main__':
    run()
