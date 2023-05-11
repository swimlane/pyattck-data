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
class Command:
    source: AnyStr = field(factory=str)
    command: AnyStr = field(factory=str)
    name: AnyStr = field(factory=str)


@define
class KillChainPhases:
    kill_chain_name: AnyStr = field()
    phase_name: AnyStr = field()


@define
class Technique(BaseModel):
    type: AnyStr = field(validator=validators.in_(['attack-pattern']))

    x_mitre_data_sources: List = field(factory=list)
    x_mitre_contributors: List = field(factory=list)
    x_mitre_impact_type: List = field(factory=list)
    x_mitre_deprecated: bool = field(factory=bool)
    x_mitre_effective_permissions: List = field(factory=list)
    x_mitre_remote_support: bool = field(factory=bool)
    x_mitre_permissions_required: List = field(factory=list)
    x_mitre_is_subtechnique: bool = field(factory=bool)
    x_mitre_detection: AnyStr = field(factory=str)
    x_mitre_defense_bypassed: List = field(factory=list)
    x_mitre_system_requirements: List = field(factory=list)
    x_mitre_attack_spec_version: SemVersion = field(factory=SemVersion)
    revoked: bool = field(factory=bool)
    object_marking_refs: List[Id] = field(factory=list)
    external_references: List[ExternalReferences] = field(factory=list)

    # used in pre-attack
    x_mitre_detectable_by_common_defenses: AnyStr = field(factory=str)
    x_mitre_detectable_by_common_defenses_explanation: AnyStr = field(factory=str)
    x_mitre_difficulty_for_adversary: AnyStr = field(factory=str)
    x_mitre_difficulty_for_adversary_explanation: AnyStr = field(factory=str)
    x_mitre_old_attack_id: AnyStr = field(factory=str)

    # these are NOT used by pre-attack but used by other frameworks
    x_mitre_modified_by_ref: Id = field(factory=Id)
    x_mitre_platforms: List[MitrePlatform] = field(factory=list)
    x_mitre_domains: List[MitreDomain] = field(factory=list)

    # used in mobile framework
    x_mitre_tactic_type: List = field(factory=list)

    # NOT used in mobile framework
    x_mitre_version: SemVersion = field(factory=SemVersion)
    description: AnyStr = field(factory=str)
    created_by_ref: Id = field(factory=Id)
    kill_chain_phases: List[KillChainPhases] = field(factory=list)

    command_list: List = field(factory=list)
    commands: List[Command] = field(factory=list) # need to define this object better
    queries: List = field(factory=list) # need to define this object better
    parsed_datasets: List = field(factory=list) # need to define this object better
    possible_detections: List = field(factory=list) # need to define this object better
    external_reference: List = field(factory=list)
    controls: List = field(factory=list)

    # Added in v13 of ATT&CK
    x_mitre_network_requirements: bool = field(factory=bool)

    # additional convenience properties 
    technique_id: AnyStr = field(factory=str)
    stix: Id = field(factory=Id)

    @property
    def actors(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='intrusion-set'
        )

    @property
    def campaigns(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='campaign'
        )

    @property
    def data_components(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='x-mitre-data-component'
        )

    @property
    def data_sources(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='x-mitre-data-source'
        )

    @property
    def malwares(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='malware'
        )

    @property
    def mitigations(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='course-of-action'
        )

    @property
    def tactics(self):
        return_list = []
        for phase in self.kill_chain_phases:
            if phase.phase_name:
                return_list.extend(self._get_tactic_objects(phase.phase_name))
        return return_list

    @property
    def techniques(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='attack-pattern'
        )

    @property
    def tools(self):
        return self._get_relationship_objects(
            parent_id=self.id,
            parent_type='tool'
        )

    def __init__(self, **kwargs):
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            print(f"There is an unknown key defined in the Technique JSON object. {te}")
            raise te

    def __attrs_post_init__(self):
        if self.id:
            self.stix = self.id
        if self.controls:
            from .control import Control
            return_list = []
            for item in self.controls:
                try:
                    return_list.append(Control(**item))
                except ValueError as ve:
                    raise ve
            self.controls = return_list
        if self.external_references:
            return_list = []
            for item in self.external_references:
                if item.get('source_name') and item.get('external_id'):
                    if item['external_id'].startswith('T'):
                        self.technique_id = item['external_id']
                return_list.append(ExternalReferences(**item))
            self.external_references = return_list
        if self.kill_chain_phases:
            return_list = []
            for item in self.kill_chain_phases:
                return_list.append(KillChainPhases(**item))
            self.kill_chain_phases = return_list
        if self.commands:
            return_list = []
            for item in self.commands:
                return_list.append(Command(**item))
            self.commands = return_list
