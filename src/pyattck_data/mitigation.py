from .types import (
    Id,
    MitreDomain
)
from .base import (
    BaseModel,
    ExternalReferences,
    List,
    AnyStr,
    SemVersion,
    define,
    field,
    validators
)


@define
class Mitigation(BaseModel):
    type: AnyStr = field(validator=validators.in_(['course-of-action']))
    description: AnyStr = field()
    created_by_ref: Id = field()
    x_mitre_deprecated: bool = field(factory=bool)
    object_marking_refs: List[Id] = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)

    # used in ics-attack
    labels: List = field(factory=list) 
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)

    # used in mobile attack
    x_mitre_old_attack_id: AnyStr = field(factory=str)

    # NOT used in mobile attack 
    x_mitre_modified_by_ref: Id = field(factory=Id)
    x_mitre_domains: List[MitreDomain] = field(factory=list)

    revoked: bool = field(factory=bool)

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
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='attack-pattern'
        )
