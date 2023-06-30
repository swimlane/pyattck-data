# ATT&CK Data Collector

This `data-collector` Python package contains similar functionality to the `generate_data` package. The main difference is that this package utilizes the ATT&CK JSON as the base object and updates/expands it from there. 

> This package is used to generate the data utilized by the `pyattck` and `goattck` packages.

## Features

This repository contains generated contextual data utilized by pyattck.

## Generated Data Access

Generated data can be retrieved from the following URLs:

* generated_attck_data_v3.json - [https://swimlane-pyattck.s3.us-west-2.amazonaws.com/generated_attck_data_v3.json](https://swimlane-pyattck.s3.us-west-2.amazonaws.com/generated_attck_data_v3.json)

# Generated ATT&CK Datasets

This page outlines and provides detailed information regarding the data generated and used with the `pyattck` and `goattck` pacakges.

## Data Categories

At this time, a shareable JSON file is generated on the `1st` and `15th` of the month and stored in a S3 bucket. This data is used and retrieved by `pyattck`

## Sources

> **First of all, I would like to thank everyone who contributes to open-source projects, especially the maintainers and creators of these projects.  Without them, this capability would not be possible.**

This data set is generated from many different sources. As we continue to add more sources, we will continue to add them here.  Again thank you to all of these projects.  In no particular order, `pyattck` utilizes data from the following projects:

* [Mitre ATT&CK APT3 Adversary Emulation Field Manual](https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx)
* [Atomic Red Team (by Red Canary)](https://github.com/redcanaryco/atomic-red-team)
* [Atomic Threat Coverage](https://github.com/atc-project/atomic-threat-coverage)
* [attck_empire (by dstepanic)](https://github.com/dstepanic/attck_empire)
* [sentinel-attack (by BlueTeamLabs)](https://github.com/BlueTeamLabs/sentinel-attack)
* [Litmus_test (by Kirtar22)](https://github.com/Kirtar22/Litmus_Test)
* [nsm-attack (by oxtf)](https://github.com/0xtf/nsm-attack)
* [osquery-attck (by teoseller)](https://github.com/teoseller/osquery-attck)
* [Mitre Stockpile](https://github.com/mitre/stockpile)
* [SysmonHunter (by baronpan)](https://github.com/baronpan/SysmonHunter)
* [ThreatHunting-Book (by 12306Bro)](https://github.com/12306Bro/Threathunting-book)
* [threat_hunting_tables (by dwestgard)](https://github.com/dwestgard/threat_hunting_tables)
* [APT Groups & Operations](https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/edit#gid=1864660085)
* [C2Matrix (by @jorgeorchilles, @brysonbort, @adam_mashinchi)](https://www.thec2matrix.com/)
* [Elemental](https://github.com/Elemental-attack/Elemental)
* [MalwareArchaeology - ATTACK](https://github.com/MalwareArchaeology/ATTACK)
* [Attack-Technique-Dataset](https://github.com/NewBee119/Attack-Technique-Dataset)
