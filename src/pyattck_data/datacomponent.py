from .base import (
    BaseModel,
    ExternalReferences,
    List,
    AnyStr,
    define,
    field,
    validators
)
from .types import (
    Id,
    SemVersion,
    MitreDomain
)


@define
class DataComponent(BaseModel):
    type: AnyStr = field(validator=validators.in_(['x-mitre-data-component']))
    description: AnyStr = field()
    created_by_ref: Id = field()
    x_mitre_modified_by_ref: Id = field()
    x_mitre_data_source_ref: Id = field()
    object_marking_refs: List[Id] = field()
    x_mitre_domains: List[MitreDomain] = field(factory=list)
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)
    object_marking_refs: List[Id] = field(factory=list)
    x_mitre_deprecated: bool = field(factory=bool)
    revoked: bool = field(factory=bool)
    external_references: List[ExternalReferences] = field(factory=list)

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
