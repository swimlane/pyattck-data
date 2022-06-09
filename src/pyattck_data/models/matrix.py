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
class Matrix(BaseModel):
    type: AnyStr = field(validator=validators.in_(['x-mitre-matrix']))
    tactic_refs: List[Id] = field()
    created_by_ref: Id = field()
    description: AnyStr = field()
    x_mitre_domains: List[MitreDomain] = field(factory=list)
    object_marking_refs: List[Id] = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)

    # used in pre-attack
    x_mitre_deprecated: bool = field(factory=bool)

    # NOT used in pre-attack
    x_mitre_version: SemVersion = field(factory=SemVersion)
    x_mitre_modified_by_ref: Id = field(factory=Id)
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)
