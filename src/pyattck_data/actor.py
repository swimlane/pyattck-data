from .types import (
    Id,
    SemVersion,
    MitreDomain
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
class Actor(BaseModel):
    type:                        AnyStr            = field(validator=validators.in_(['intrusion-set']))
    aliases:                     List              = field(factory=list)
    x_mitre_contributors:        List              = field(factory=list)
    revoked:                     bool              = field(factory=bool)
    description:                 AnyStr            = field(factory=str)
    x_mitre_modified_by_ref:     Id                = field(factory=Id) 
    x_mitre_deprecated:          bool              = field(factory=bool)
    x_mitre_attack_spec_version: SemVersion        = field(factory=SemVersion)
    created_by_ref:              Id                = field(factory=Id)
    x_mitre_domains:             List[MitreDomain] = field(factory=list)
    object_marking_refs:         List[Id]          = field(factory=list)
    external_references:         List[ExternalReferences] = field(factory=list)

    # These additional properties are from external data sets
    names:                       List              = field(factory=list)
    #tools:                       List              = field(factory=list)
    external_tools:              List              = field(factory=list)
    country:                     List              = field(factory=list)
    operations:                  List              = field(factory=list)
    links:                       List              = field(factory=list)
    targets:                     List              = field(factory=list)
    external_description:        List              = field(factory=list)
    attck_id:                    AnyStr            = field(factory=str)
    comment:                     AnyStr            = field(factory=str)

    def __attrs_post_init__(self):
        if self.external_references:
            return_list = []
            for item in self.external_references:
                return_list.append(ExternalReferences(**item))
            self.external_references = return_list

    @property
    def malwares(self):
        """
        Returns all malware objects that are known to used by this actor.

        Returns:
            [list[Malware]] -- A list of malware objects defined within the
                      Enterprise MITRE ATT&CK Framework
        """
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='malware'
        )
 
    @property
    def tools(self):
        """
        Returns all tool objects that are known to used by this actor.

        Returns:
            [list[Tool]] -- A list of tool objects defined within the
                      Enterprise MITRE ATT&CK Framework
        """
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='tool'
        )

    @property
    def techniques(self):
        """
        Returns all technique objects that this actor is known to use.

        Returns:
            [list[Technique]] -- A list of technique objects defined within the
                      Enterprise MITRE ATT&CK Framework
        """
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='attack-pattern'
        )
