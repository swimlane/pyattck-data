"""This class is the main entrypoint for this project."""
import atexit
import json

import requests
from attrs import asdict

from pyattck_data.attack import MitreAttck

from .base import Base
from .services.adversaryemulation import AdversaryEmulation
from .services.aptthreattracking import APTThreatTracking
from .services.atomicredteam import AtomicRedTeam
from .services.atomicthreatcoverage import AtomicThreatCoverage
from .services.attckdatasources import AttckDatasources
from .services.attckempire import AttckEmpire
from .services.blueteamlabs import BlueTeamLabs
from .services.c2matrix import C2Matrix
from .services.elemental import ElementalAttack
from .services.litmustest import LitmusTest
from .services.malwarearchaeology import MalwareArchaeology
from .services.newbeeattackdata import NewBeeAttackDataset
from .services.nsmattck import NSMAttck
from .services.osqueryattack import OsqueryAttack
from .services.stockpile import MitreStockpile
from .services.sysmonhunter import SysmonHunter
from .services.splunkcontent import SplunkSecurityContent


class Collector(Base):

    def _create_attck_object(self) -> None:
        if not Base.ENTERPRISE_ATTCK_JSON:
            Base.ENTERPRISE_ATTCK_JSON = requests.get("https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json").json()
            Base.attck = MitreAttck(**Base.ENTERPRISE_ATTCK_JSON)

    def collect(self) -> None:
        atexit.register(self.write)
        self._create_attck_object()
        for service in [
            AdversaryEmulation,
            APTThreatTracking,
            AtomicRedTeam,
            AtomicThreatCoverage,
            AttckDatasources,
            AttckEmpire,
            BlueTeamLabs,
            C2Matrix,
            ElementalAttack,
            LitmusTest,
            MalwareArchaeology,
            NewBeeAttackDataset,
            NSMAttck,
            OsqueryAttack,
            MitreStockpile,
            SysmonHunter,
            SplunkSecurityContent,
        ]:
            self.__logger.info(f"Collecting data from {service.__name__}")
            service().parse()

    def write(self) -> None:
        with open("generated_attck_data_v3.json", "w+") as f:
            json.dump(asdict(Base.attck), f, indent=4, allow_nan=False)
