from datetime import datetime
from typing import (
    Any,
    AnyStr,
    List
)
from pydantic import (
    HttpUrl
)
from attr import (
    define,
    field,
    validators
)
from .types import (
    PATTERNS,
    Id,
    MitreRelationship,
    SemVersion
)


BASE_OBJECTS = []
RELATIONSHIP_MAP = {}


@define
class ExternalReferences:
    source_name: AnyStr = field(factory=str)
    url: HttpUrl = field(factory=str)
    external_id: AnyStr = field(factory=str)
    description: AnyStr = field(factory=str)


@define
class BaseAttckModel:
    id: Id = field()


@define(eq=False)
class BaseModel(BaseAttckModel):
    id: Id = field()
    name: AnyStr = field()
    created: datetime = field()
    modified: datetime = field()
    x_mitre_version: SemVersion = field()
    x_mitre_domains: List = field()

    def _get_relationship_objects(self, parent_id: str, parent_type: str) -> list:
        return_list = []
        if RELATIONSHIP_MAP.get(parent_id):
            for item in RELATIONSHIP_MAP[parent_id]:
                for x in BASE_OBJECTS:
                    if x.id == item and x.type == parent_type and x not in return_list:
                        return_list.append(x)
        return return_list

    def _get_tactic_objects(self, name):
        return_list = []
        for item in BASE_OBJECTS:
            if item.type == "x-mitre-tactic":
                if hasattr(item, "x_mitre_shortname") and item.x_mitre_shortname == name.lower():
                    return_list.append(item)
        return return_list

    def __attrs_post_init__(self):
        if self.external_references:
            return_list = []
            for item in self.external_references:
                return_list.append(ExternalReferences(**item))
            self.external_references = return_list


@define
class BaseRelationship:
    id: Id = field()
    type: AnyStr = field(validator=validators.in_(['relationship']))
    created: datetime = field()
    modified: datetime = field()
    source_ref: Id = field()
    target_ref: Id = field()
    relationship_type: MitreRelationship = field()
