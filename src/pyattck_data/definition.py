from datetime import datetime
from attr import validators
from .types import (
    Id,
    SemVersion, 
    PATTERNS
)
from .base import (
    ExternalReferences,
    List,
    AnyStr,
    define,
    field
)


@define
class Statement:
    statement: AnyStr = field()


@define
class MarkingDefinition:
    type: AnyStr = field(validator=validators.in_(['marking-definition']))
    id: Id = field()
    type: AnyStr = field(validator=validators.in_(PATTERNS['types']['examples']))
    created: datetime = field()
    definition: Statement = field()
    definition_type: AnyStr = field()

    created_by_ref: Id = field(factory=Id)
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)
    object_marking_refs: List = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)

    revoked: bool = field(factory=bool)

    def __init__(self, **kwargs):
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            print(te)
            raise te

    def __attrs_post_init__(self):
        if self.external_references:
            return_list = []
            for item in self.external_references:
                return_list.append(ExternalReferences(**item))
            self.external_references = return_list
