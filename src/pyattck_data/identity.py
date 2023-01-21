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

    def __init__(self, **kwargs):
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            print(f"There is an unknown key defined in the Identity JSON object. {te}")
            raise te

    def __attrs_post_init__(self):
        if self.external_references:
            return_list = []
            for item in self.external_references:
                return_list.append(ExternalReferences(**item))
            self.external_references = return_list
