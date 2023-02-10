# -*- coding: utf-8 -*-
import requests

from pyattck_data.attack import MitreAttck
from pyattck_data.generated import GeneratedData
from pyattck_data.nist import NistControls, GeneratedNistControlMap
from pyattck_data.malware import Malware
from pyattck_data.tool import Tool
from pyattck_data.actor import Actor
from pyattck_data.datacomponent import DataComponent
from pyattck_data.datasource import DataSource
from pyattck_data.mitigation import Mitigation
from pyattck_data.tactic import Tactic
from pyattck_data.technique import Technique
from pyattck_data.campaign import Campaign
    
ENTERPRISE_ATTCK_JSON = requests.get("https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_enterprise_attck_v1.json").json()
PRE_ATTCK_JSON = requests.get("https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_pre_attck_v1.json").json()
MOBILE_ATTCK_JSON = requests.get("https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_mobile_attck_v1.json").json()
ICS_ATTCK_JSON = requests.get("https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_ics_attck_v1.json").json()
GENERATED_NIST_JSON = requests.get("https://swimlane-pyattck.s3.us-west-2.amazonaws.com/attck_to_nist_controls.json").json()
NIST_CONTROLS_JSON = requests.get("https://raw.githubusercontent.com/center-for-threat-informed-defense/attack-control-framework-mappings/main/frameworks/attack_10_1/nist800_53_r4/stix/nist800-53-r4-controls.json").json()



ENTERPRISE_OBJ = MitreAttck(**ENTERPRISE_ATTCK_JSON)


def test_enterprise():
    assert MitreAttck(**ENTERPRISE_ATTCK_JSON)

def test_ics():
    assert MitreAttck(**ICS_ATTCK_JSON)

def test_mobile():
    assert MitreAttck(**MOBILE_ATTCK_JSON)

def test_pre_attck():
    assert MitreAttck(**PRE_ATTCK_JSON)

def test_nist_controls():
    assert NistControls(**NIST_CONTROLS_JSON)

def test_controls():
    assert GeneratedNistControlMap(**{"data": GENERATED_NIST_JSON})

def test_actor():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'intrusion-set':
            for malware in item.malwares:
                assert isinstance(malware, Malware)
            try:
                if item.tools:
                    for tool in item.tools:
                        assert isinstance(tool, Tool)
            except:
                pass
            for technique in item.techniques:
                assert isinstance(technique, Technique)

def test_campaign():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'campaign':
            for technique in item.techniques:
                assert isinstance(technique, Technique)
            for malware in item.malwares:
                assert isinstance(malware, Malware)

def test_datacomponent():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'x-mitre-data-component':
            for technique in item.techniques:
                assert isinstance(technique, Technique)

def test_datasource():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'x-mitre-data-source':
            for technique in item.techniques:
                assert isinstance(technique, Technique)
            for component in item.data_components:
                assert isinstance(component, DataComponent)

def test_malware():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'malware':
            for technique in item.techniques:
                assert isinstance(technique, Technique)
            for actor in item.actors:
                assert isinstance(actor, Actor)
            for campaign in item.campaigns:
                assert isinstance(campaign, Campaign)

def test_mitigation():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'course-of-action':
            for technique in item.techniques:
                assert isinstance(technique, Technique)

def test_tactic():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'x-mitre-tactic':
            for technique in item.techniques:
                assert isinstance(technique, Technique)

def test_technique():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'attack-pattern':
            for actor in item.actors:
                assert isinstance(actor, Actor)
            for campaign in item.campaigns:
                assert isinstance(campaign, Campaign)
            for component in item.data_components:
                assert isinstance(component, DataComponent)
            for source in item.data_sources:
                assert isinstance(source, DataSource)
            for malware in item.malwares:
                assert isinstance(malware, Malware)
            for mitigation in item.mitigations:
                assert isinstance(mitigation, Mitigation)
            for tactic in item.tactics:
                assert isinstance(tactic, Tactic)
            for technique in item.techniques:
                assert isinstance(technique, Technique)
            for tool in item.tools:
                assert isinstance(tool, Tool)

def test_tactic():
    for item in ENTERPRISE_OBJ.objects:
        if item.type == 'tool':
            for technique in item.techniques:
                assert isinstance(technique, Technique)
            for actor in item.actors:
                assert isinstance(actor, Actor)
