import json
import os
from requests import request

from attrs import asdict

from .base import Base
from .services import (
    AdversaryEmulation,
    AtomicRedTeam,
    MitreStockpile,
    ThreatHuntingTables,
    SysmonHunter,
    BlueTeamLabs,
    AtomicThreatCoverage,
    OsqueryAttack,
    AttckEmpire,
    ThreatHuntingBook,
    NSMAttck,
    LitmusTest,
    C2Matrix,
    APTThreatTracking,
    ElementalAttack,
    MalwareArchaeology,
    NewBeeAttackDataset,
    AttckDatasources
)


class PyattckData(Base):

    enterprise_attck = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    pre_attck="https://raw.githubusercontent.com/mitre/cti/master/pre-attack/pre-attack.json"
    mobile_attck="https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json"
    ics_attck="https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json"

    def go(self):
        for service in [
            AdversaryEmulation,
            AtomicRedTeam,
            MitreStockpile,
            ThreatHuntingTables,
            SysmonHunter,
            BlueTeamLabs,
            AtomicThreatCoverage,
            OsqueryAttack,
            AttckEmpire,
            ThreatHuntingBook,
            NSMAttck,
            LitmusTest,
            C2Matrix,
            APTThreatTracking,
            ElementalAttack,
            MalwareArchaeology,
            NewBeeAttackDataset,
            AttckDatasources
        ]:
            print(f"Processing {service} now.")
            getattr(service(), 'get')()
        return asdict(self.generated_data)

    def _update_attack_patterns(self, item, generated_data):
        if item.get('external_references'):
            for ref in item['external_references']:
                if ref.get('external_id') and ref['external_id'].startswith('T'):
                    for tech in generated_data['techniques']:
                        if tech['technique_id'] == ref['external_id']:
                            return {
                                'command_list': tech['command_list'],
                                'commands': tech['commands'],
                                'parsed_datasets': tech['parsed_datasets'],
                                'queries': tech['queries'],
                                'possible_detections': tech['possible_detections'],
                                'external_reference': tech['external_reference']
                            }
        return {}

    def _update_c2_data(self, item, generated_data):
        if item.get('name'):
            for tool in generated_data['c2_data']:
                if tool['name'] == item['name'] or item.get('x_mitre_aliases') and tool['name'] in item['x_mitre_aliases']:
                    return tool
        return {}

    def _update_tool(self, item, generated_data):
        if item.get('name'):
            for tool in generated_data['tools']:
                for name in tool['names']:
                    if name in item['name'] or item.get('x_mitre_aliases') and name in item['x_mitre_aliases']:
                        return tool
        return {}

    def _update_actor(self, item, generated_data):
        external_id = None
        if item.get('external_references'):
            for ref in item['external_references']:
                if ref.get('external_id') and ref['external_id'].startswith('G'):
                    external_id = ref['external_id']
        for actor in generated_data['actors']:
            if actor.get('attck_id') and actor['attck_id'] == external_id:
                return actor
        return {}

    def _download_url_data(self, url):
        response = request('GET', url)
        if response.status_code == 200:
            return response.json()
        return {}

    def _save_to_disk(self, path, data):
        with open(path, 'w+') as f:
            json.dump(data, f)

    def _save_json_data(self, force: bool=False) -> None:
        for json_data in ['enterprise_attck', 'pre_attck', 
                          'mobile_attck', 'ics_attck']:
            try:
                path = os.path.join(f"{json_data}.json")
                if not os.path.exists(path) or force:
                    data = self._download_url_data(getattr(self, json_data))
                    self._save_to_disk(path, data)
            except:
                raise Warning(f"Unable to download data from {json_data}")
        return True

    def save(self):
        data = self.go()
        with open('generated_attck_data.json', 'w') as f:
            f.write(json.dumps(data))

    def merge(self):
        self._save_json_data()
        data = None
        with open('generated_attck_data_v2.json') as f:
            data = json.load(f)
        for framework in ['enterprise_attck', 'pre_attck', 
                          'mobile_attck', 'ics_attck']:
            attck = None
            with open(f'{framework}.json') as f:
                attck = json.load(f)
            for item in attck.get('objects'):
                if item.get('type'):
                    if item['type'] == 'attack-pattern':
                        item.update(**self._update_attack_patterns(item, data))
                    elif item['type'] == 'tool' or item['type'] == 'malware':
                        item.update(**self._update_c2_data(item, data))
                        item.update(**self._update_tool(item, data))
                    elif item['type'] == 'intrusion-set':
                        item.update(**self._update_actor(item, data))
            with open(f'merged_{framework}_v1.json', 'w+') as f:
                f.write(json.dumps(attck))
