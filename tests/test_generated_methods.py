import json

from pyattck_data.models.generated import GeneratedData


GENERATED_ATTCK_JSON = json.load(open("tests/resources/generated_attck_data.json"))

SAMPLE_DATA = {
    "country": "china",
    "names": ["APT1"],
    "targets": ["USA"],
    "operations": ["Some overseas operation"],
    "description": "my description",
    "tools": ["PowerShell", "Python"],
    "links": ["https://google.com"],
    "attck_id": "T1009",
    "comment": "Some comment",
    "family": ["USA"],
    "names": ["PowerShell", "Python"],
    "links": ["https://google.com"],
    "comments": "Some comment",
    "technique_id": "T1009",
    "source": "https://google.com",
    "name": "",
    "command": "shell ver",
    "content": {
        "Category": "T1033",
        "Built-in Windows Command": "whoami /all /fo list",
        "Cobalt Strike": "shell whoami /all /fo list",
        "Metasploit": "getuid",
        "Description": "Get current user information, SID, domain, groups the user belongs to, security privs of the user"
    },
    "product": "Azure Sentinel",
    "content": "Sysmon| where EventID == 1 and (process_path contains \"whoami.exe\"or process_command_line contains \"whoami\"or file_directory contains \"useraccount get /ALL\"or process_path contains \"qwinsta.exe\"or process_path contains \"quser.exe\"or process_path contains \"systeminfo.exe\")",
    "name": "System Owner User Discovery",
    "data": {
        "title": "System Owner or User Discovery",
        "id": "9a0d8ca0-2385-4020-b6c6-cb6153ca56f3",
        "status": "experimental",
        "description": "Adversaries may use the information from System Owner/User Discovery during automated discovery to shape follow-on behaviors, including whether or not the adversary fully infects the target and/or attempts specific actions.",
        "author": "Timur Zinniatullin, oscd.community",
        "date": "2019/10/21",
        "references": [
            "https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1033/T1033.yaml"
        ],
        "logsource": {
            "product": "linux",
            "service": "auditd"
        },
        "detection": {
            "selection": {
                "type": "EXECVE",
                "a0": [
                    "users",
                    "w",
                    "who"
                ]
            },
            "condition": "selection"
        },
        "falsepositives": [
            "Admin activity"
        ],
        "level": "low",
        "tags": [
            "attack.discovery",
            "attack.t1033"
        ]
    },
    "reference": "https://researchcenter.paloaltonetworks.com/2017/02/unit42-magic-hound-campaign-attacks-saudi-targets/",
    "c2_data": {
        "name": "Alan",
        "license": "Created Commons",
        "price": "NA",
        "github": "https://github.com/enkomio/AlanFramework",
        "site": "",
        "twitter": "@s4tan",
        "evaluator": "@s4tan",
        "date": "9/10/2021",
        "version": "4",
        "implementation": "binary",
        "how_to": "",
        "slingshot": "",
        "kali": "",
        "server": ".NET",
        "implant": "C/Asm",
        "multi_user": "No",
        "ui": "No",
        "dark_mode": "No",
        "api": "No",
        "windows": "Yes",
        "linux": "No",
        "macos": "No",
        "tcp": "No",
        "http": "Yes",
        "http2": "No",
        "http3": "No",
        "dns": "No",
        "doh": "No",
        "icmp": "No",
        "ftp": "No",
        "imap": "No",
        "mapi": "No",
        "smb": "No",
        "ldap": "No",
        "key_exchange": "Yes",
        "stego": "No",
        "proxy_aware": "No",
        "domainfront": "No",
        "custom_profile": "Yes",
        "jitter": "Yes",
        "working_hours": "No",
        "kill_date": "No",
        "chaining": "No",
        "logging": "Yes",
        "in_wild": "",
        "attck_mapping": "",
        "dashboard": "",
        "blog": "",
        "c2_matrix_indicators": "",
        "jarm": "",
        "actively_maint": "Yes",
        "slack": "No",
        "slack_members": "No",
        "gh_issues": "",
        "notes": "All code is executed in memory"
    }
}

def test_add_actor_item():
    data = GeneratedData()
    data.add_actor_item(
        country=SAMPLE_DATA["country"],
        names=SAMPLE_DATA["names"],
        targets=SAMPLE_DATA["targets"],
        operations=SAMPLE_DATA["operations"],
        description=SAMPLE_DATA["description"],
        tools=SAMPLE_DATA["tools"],
        links=SAMPLE_DATA["links"],
        attck_id=SAMPLE_DATA["attck_id"],
        comment=SAMPLE_DATA["comment"]
    )
    assert data.last_updated
    assert data.actors
    assert len(data.actors) == 1
    for actor in data.actors:
        assert actor.attck_id == SAMPLE_DATA["attck_id"]
        assert hasattr(actor, 'attck_id')
        for key,val in SAMPLE_DATA.items():
            if hasattr(actor, key):
                assert len(getattr(actor, key)) == len(val)


def test_add_tool_item():
    data = GeneratedData()
    data.add_tool_item(
        names=SAMPLE_DATA["names"], 
        comments=SAMPLE_DATA["comment"], 
        family=SAMPLE_DATA["family"], 
        links=SAMPLE_DATA["links"]
    )
    assert data.last_updated
    assert data.tools
    assert len(data.tools) == 1
    for tool in data.tools:
        for key,val in SAMPLE_DATA.items():
            if hasattr(tool, key):
                assert len(getattr(tool, key)) == len(val)

def test_add_command():
    data = GeneratedData()
    data.add_command(
        technique_id=SAMPLE_DATA["technique_id"],
        source=SAMPLE_DATA["source"],
        command=SAMPLE_DATA["command"],
        name=SAMPLE_DATA["name"]
    )
    assert data.last_updated
    assert data.techniques
    assert len(data.techniques) == 1
    for technique in data.techniques:
        assert technique.technique_id == SAMPLE_DATA["technique_id"]
        assert technique.commands
        for command in technique.commands:
            assert command.command == SAMPLE_DATA["command"]
            assert command.command in technique.command_list
            assert command.source == SAMPLE_DATA["source"]
            assert command.name == SAMPLE_DATA["name"]

def test_add_dataset():
    data = GeneratedData()
    data.add_dataset(
        technique_id=SAMPLE_DATA["technique_id"],
        content=SAMPLE_DATA["content"]
    )
    assert data.last_updated
    assert data.techniques
    assert len(data.techniques) == 1
    for technique in data.techniques:
        assert technique.technique_id == SAMPLE_DATA["technique_id"]
        assert technique.parsed_datasets
        for dataset in technique.parsed_datasets:
            assert dataset == SAMPLE_DATA["content"]

def test_add_possible_queries():
    local_data = {
        "content": "Sysmon| where EventID == 1 and (process_path contains \"whoami.exe\"or process_command_line contains \"whoami\"or file_directory contains \"useraccount get /ALL\"or process_path contains \"qwinsta.exe\"or process_path contains \"quser.exe\"or process_path contains \"systeminfo.exe\")",
    }
    data = GeneratedData()
    data.add_possible_queries(
        technique_id=SAMPLE_DATA["technique_id"],
        product=SAMPLE_DATA["product"],
        content=local_data["content"],
        name=SAMPLE_DATA["name"]
    )
    assert data.last_updated
    assert data.techniques
    assert len(data.techniques) == 1
    for technique in data.techniques:
        assert technique.technique_id == SAMPLE_DATA["technique_id"]
        assert technique.queries
        for query in technique.queries:
            assert query.product == SAMPLE_DATA["product"]
            assert query.name == SAMPLE_DATA["name"]
            assert query.query == local_data["content"]

def test_add_possible_detection():
    data = GeneratedData()
    data.add_possible_detection(
        technique_id=SAMPLE_DATA["technique_id"],
        data=SAMPLE_DATA["data"]
    )
    assert data.last_updated
    assert data.techniques
    assert len(data.techniques) == 1
    for technique in data.techniques:
        assert technique.technique_id == SAMPLE_DATA["technique_id"]
        assert technique.possible_detections
        assert technique.possible_detections[0] == SAMPLE_DATA["data"]

def test_add_external_reference():
    data = GeneratedData()
    data.add_external_reference(
        technique_id=SAMPLE_DATA["technique_id"],
        reference=SAMPLE_DATA["reference"]
    )
    assert data.last_updated
    assert data.techniques
    assert len(data.techniques) == 1
    for technique in data.techniques:
        assert technique.technique_id == SAMPLE_DATA["technique_id"]
        assert technique.external_reference
        assert technique.external_reference[0] == SAMPLE_DATA["reference"]

def test_add_c2_data():
    data = GeneratedData()
    data.add_c2_data(SAMPLE_DATA["c2_data"])
    assert data.last_updated
    assert data.c2_data
    assert len(data.c2_data) == 1
    for c2 in data.c2_data:
        for key,val in SAMPLE_DATA["c2_data"].items():
            assert hasattr(c2, key)
            assert getattr(c2, key) == val
