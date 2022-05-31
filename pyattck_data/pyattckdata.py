import json

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

    def save(self):
        with open('generated_attck_data.json', 'w') as f:
            f.write(json.dumps(self.go()))
