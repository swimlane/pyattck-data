from .types import (
    Id,
    SemVersion
)
from .base import (
    BaseRelationship,
    ExternalReferences,
    List,
    AnyStr,
    define,
    field
)


@define
class Relationship(BaseRelationship):
    object_marking_refs: List[Id] = field()
    revoked: bool = field(factory=bool)
    created_by_ref: Id = field(factory=Id)
    description: AnyStr = field(factory=str)
    x_mitre_deprecated: bool = field(factory=bool)
    x_mitre_version: SemVersion = field(factory=SemVersion)
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)
    external_references: List[ExternalReferences] = field(factory=list)

    # NOT used by pre-attack
    x_mitre_modified_by_ref: Id = field(factory=Id)

    def __init__(self, **kwargs):
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            raise te

    def __attrs_post_init__(self):
        if self.external_references:
            return_list = []
            for item in self.external_references:
                return_list.append(ExternalReferences(**item))
            self.external_references = return_list
