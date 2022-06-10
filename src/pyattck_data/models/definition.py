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