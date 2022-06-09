from pyattck_data.models.attack import MitreAttck, TYPE_MAP
from pyattck_data.models.nist import NistControls, GeneratedNistControlMap, ControlObject, BaseRelationship


data = None

import requests

def test_each_model():
    default_config_data = {
        "enterprise_attck_json": "https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_enterprise_attck_v1.json",
        "pre_attck_json": "https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_pre_attck_v1.json",
        "mobile_attck_json": "https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_mobile_attck_v1.json",
        "ics_attck_json": "https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_ics_attck_v1.json",
        "nist_controls_json": "https://swimlane-pyattck.s3.us-west-2.amazonaws.com/merged_nist_controls_v1.json",
        "generated_nist_json": "https://swimlane-pyattck.s3.us-west-2.amazonaws.com/attck_to_nist_controls.json",
    }
    for key,val in default_config_data.items():
        response = requests.get(val).json()
        skip = False
        if key == 'nist_controls_json':
            data = NistControls(**response)
        elif key == 'generated_nist_json':
            data = GeneratedNistControlMap(**{"data": response})
            skip = True
        else:
            data  = MitreAttck(**response)
        if not skip:
            for item in response['objects']:
                if item.get('type'):
                    if key == 'nist_controls_json':
                        if item['type'] == 'relationship':
                            try:
                                BaseRelationship(**item)
                            except TypeError as te:
                                print(item)
                                print(te)
                                assert False
                        else:
                            try:
                                ControlObject(**item)
                            except TypeError as te:
                                print(item)
                                print(te)
                                assert False
                    else:
                        if TYPE_MAP.get(item['type']):
                            try:
                                TYPE_MAP[item['type']](**item)
                            except TypeError as te:
                                print(item)
                                print(te)
                                assert False
