from datetime import datetime
from attr import validators
from .types import (
    Id
)
from .base import (
    ExternalReferences,
    List,
    AnyStr,
    define,
    field
)


@define
class Identity:
    id: Id = field()
    type: AnyStr = field(validator=validators.in_(['identity']))
    identity_class: AnyStr = field()
    created: datetime = field()
    modified: datetime = field()
    name: AnyStr = field()
    object_marking_refs: List[Id] = field()
    roles: List = field(factory=list)
    sectors: List = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)
