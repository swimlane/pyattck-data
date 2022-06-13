from datetime import datetime

from attrs import validators

from .types import Id, SemVersion
from .base import (
    List,
    AnyStr,
    BaseRelationship,
    define,
    field,
    ExternalReferences
)


@define
class ControlObject:
    id: Id = field()
    name: AnyStr = field()
    created: datetime = field()
    external_references: List[ExternalReferences] = field()
    modified: datetime = field()
    description: AnyStr = field()
    type: AnyStr = field(validator=validators.in_(['course-of-action']))
    x_mitre_family: AnyStr = field()
    x_mitre_priority: AnyStr = field(factory=str)
    x_mitre_impact: list = field(factory=list)


@define
class NistControls:
    id: Id = field()
    type: Id = field()
    objects: List[ControlObject] = field(factory=list)
    spec_version: SemVersion = field(factory=SemVersion)

    def __attrs_post_init__(self):
        if self.objects:
            return_list = []
            for item in self.objects:
                if item.get('type') == 'relationship':
                    try:
                        return_list.append(BaseRelationship(**item))
                    except Exception as e:
                        raise e
                else:
                    try:
                        return_list.append(ControlObject(**item))
                    except Exception as e:
                        print(item)
                        raise e
            self.objects = return_list

@define
class GeneratedNistControlMap:
    data: dict = field()

    def __attrs_post_init__(self):
        if self.data:
            return_dict = {}
            for key,val in self.data.items():
                try:
                    Id().validate(key)
                except Exception as e:
                    raise e
                return_dict[key] = []
                if isinstance(val, list):
                    for item in val:
                        try:
                            Id().validate(item)
                        except Exception as e:
                            raise e
                    return_dict[key] = val
            self.data = return_dict
