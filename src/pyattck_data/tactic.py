from math import factorial
from .types import (
    Id,
    SemVersion
)
from .base import (
    BASE_OBJECTS,
    BaseModel,
    ExternalReferences,
    List,
    AnyStr,
    define,
    field,
    validators
)


@define
class Tactic(BaseModel):
    type: AnyStr = field(validator=validators.in_(['x-mitre-tactic']))
    description: AnyStr = field()
    created_by_ref: Id = field()
    x_mitre_shortname: AnyStr = field()
    object_marking_refs: List[Id] = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)
    x_mitre_contributors: List = field(factory=list)

    # used in ics-attack
    x_mitre_deprecated: bool = field(factory=bool)
    revoked: bool = field(factory=bool)

    # NOT used in pre-attack
    x_mitre_version: SemVersion = field(factory=SemVersion)
    x_mitre_domains: List = field(factory=list)
    x_mitre_modified_by_ref: Id = field(factory=Id)
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)

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

    @property
    def techniques(self):
        return_list = []
        for object in BASE_OBJECTS:
            if hasattr(object, 'kill_chain_phases'):
                for prop in object.kill_chain_phases:
                    if prop.phase_name.lower() == self.x_mitre_shortname.lower():
                        return_list.append(object)
        return return_list
