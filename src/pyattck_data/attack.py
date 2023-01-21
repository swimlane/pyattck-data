from .types import (
    SemVersion
)
from .base import (
    List,
    AnyStr,
    define,
    field,
    BaseAttckModel,
    RELATIONSHIP_MAP,
    BASE_OBJECTS
)
from .actor import Actor
from .datacomponent import DataComponent
from .datasource import DataSource
from .definition import MarkingDefinition
from .identity import Identity
from .malware import Malware
from .matrix import Matrix
from .mitigation import Mitigation
from .relationship import Relationship
from .tactic import Tactic
from .technique import Technique
from .tool import Tool
from .campaign import Campaign


TYPE_MAP = {
    'intrusion-set': Actor,
    'x-mitre-data-component': DataComponent,
    'x-mitre-data-source': DataSource,
    'marking-definition': MarkingDefinition,
    'identity': Identity,
    'malware': Malware,
    'x-mitre-matrix': Matrix,
    'course-of-action': Mitigation,
    'relationship': Relationship,
    'x-mitre-tactic': Tactic,
    'attack-pattern': Technique,
    'tool': Tool,
    'campaign': Campaign
}


@define
class MitreAttck(BaseAttckModel):
    type: AnyStr = field()
    spec_version: SemVersion = field()
    objects: List = field()
    relationship_map: dict = field(factory=dict)
    revoked: bool = field(factory=bool)

    def __init__(self, **kwargs):
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            raise te

    def __attrs_post_init__(self):
        if self.objects:
            return_list = []
            for item in self.objects:
                try:
                    data = TYPE_MAP.get(item['type'])(**item)
                    return_list.append(data)
                    BASE_OBJECTS.append(data)
                except TypeError as te:
                    raise te
                if item['type'] == 'relationship' and item['relationship_type'] != 'revoked-by':
                    source_id = item['source_ref']
                    target_id = item['target_ref']
                    if source_id not in RELATIONSHIP_MAP:
                        RELATIONSHIP_MAP[source_id] = []
                    if target_id not in RELATIONSHIP_MAP[source_id]:
                        RELATIONSHIP_MAP[source_id].append(target_id)
                    if target_id not in RELATIONSHIP_MAP:
                        RELATIONSHIP_MAP[target_id] = []
                    if source_id not in RELATIONSHIP_MAP[target_id]:
                        RELATIONSHIP_MAP[target_id].append(source_id)
            self.objects = return_list
