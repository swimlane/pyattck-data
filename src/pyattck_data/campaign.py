from datetime import datetime

from .types import (
    Id, 
    SemVersion,
    MitreDomain,
    MitrePlatform
)
from .base import (
    BaseModel,
    ExternalReferences,
    List,
    AnyStr,
    define,
    field,
    validators
)


@define
class Campaign(BaseModel):

    # Fields
    type: AnyStr = field(validator=validators.in_(['campaign']))
    description: AnyStr = field()
    first_seen: datetime = field()
    last_seen: datetime = field()
    x_mitre_first_seen_citation: AnyStr = field()
    x_mitre_last_seen_citation: AnyStr = field()
    aliases: List = field(factory=list)
    x_mitre_deprecated: bool = field(factory=bool)
    x_mitre_contributors: List = field(factory=list)
    revoked: bool = field(factory=bool)
    created_by_ref: Id = field(factory=Id)
    external_references: List[ExternalReferences] = field(factory=list)
    object_marking_refs: List[Id] = field(factory=list)
    
    # NOT used in mobile attack
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)
    x_mitre_modified_by_ref: Id = field(factory=Id)

    # Inheritables from BaseModel
    # name: List = field()
    # created: datetime = field()
    # modified: datetime = field()
    # x_mitre_version: SemVersion = field()
    x_mitre_domains: List[MitreDomain] = field(factory=list) # A better definition

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
    def malwares(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='malware'
        )

    @property
    def tools(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='tool'
        )

    @property
    def techniques(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='attack-pattern'
        )
