from .base import (
    BaseModel,
    ExternalReferences,
    Id,
    List,
    AnyStr,
    define,
    field
)


@define
class Control(BaseModel):
    revoked: bool = field()
    x_mitre_family: AnyStr = field(factory=str)
    x_mitre_impact: List = field(factory=list)
    x_mitre_priority: AnyStr = field(factory=str)
    object_marking_refs: List[Id] = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)

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
