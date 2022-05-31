import csv

import requests

from ..base import Base


class APTThreatTracking(Base):

    """
    Data Source: https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/edit#
    Author: Uknown

    This class is a wrapper for the above data set
    """

    _URL = 'https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/export?format=csv&id=1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU&gid={gid}'

    __GID_MAP  = {
        'readme': '1864660085',
        'china': '361554658',
        'russia': '1636225066',
        'north_korea': '1905351590',
        'iran': '376438690',
        'israel': '300065512',
        'nato': '2069598202',
        'middle_east': '574287636',
        'other': '438782970',
        'unknown': '1121522397',
        'dll_side_loading': '680227912',
        'naming_schema': '810474396',
        'malware': '659129093',
        'sources': '667848006',
    }

    def get(self):
        return_list = []
        for key,val in self.__GID_MAP.items():
            if key != 'readme':
                response = requests.get(self._URL.format(gid=val))
                data = response.text
                return_list.append(self._parse(key,data))
        return return_list
        
    def _parse(self, sheet_name, data):
        count = 0
        headers = None
        dict_list = []
        for item in csv.reader(data.splitlines()):
            count += 1
            if sheet_name == 'malware':
                if count < 3:
                    continue
                if count == 3:
                    headers = item
                    continue
                c2_dict = dict(zip(headers, item))
                dict_list.append(c2_dict)
            else:
                if count == 1:
                    continue
                if count == 2:
                    headers = item
                    continue
                c2_dict = dict(zip(headers, item))
                dict_list.append(c2_dict)
    
        if sheet_name not in ['malware', 'dll_side_loading', 'naming_schema', 'sources']:
            self.__parse_data(sheet_name, dict_list=dict_list)
        else:
            self.__parse_malware_tool_data(dict_list=dict_list)

    def __parse_malware_tool_data(self, dict_list):
        tool_names = []
        family_names = []
        comments = None
        links = []
        for item in dict_list:
            for key, val in item.items():
                if 'name' in key.lower() and val:
                    tool_names.append(val)
                elif 'dll' in key.lower() and val:
                    tool_names.append(val)
                elif 'product' in key.lower() and val:
                    tool_names.append(val)
                elif 'family' in key.lower() and val:
                    family_names.append(val)
                elif 'comment' in key.lower() and val:
                    comments = val
                elif 'link' in key.lower() and val:
                    links.append(val)
            if tool_names or family_names or comments or links:
                self.generated_data.add_tool_item(
                    names=tool_names,
                    comments=comments,
                    family=family_names,
                    links=links
                )
            tool_names = []
            family_names = []
            comments = None
            links = []

    def __parse_data(self, country, dict_list):
        actor_names = []
        target = []
        operations = []
        description = None
        links = []
        tools = []
        attck_id = None
        comment = None
        for item in dict_list:
            for key,val in item.items():
                if 'name' in key.lower() and val:
                    actor_names.append(val)
                elif key.lower() in ['crowdstrike','talos','dell', 'irl','kaspersky','secureworks','mandiant','fireeye','symantec','isight','cisco','palo','overlaps'] and val:
                    if ',' in val:
                        name_list = [x.strip() for x in val.split(',')]
                        for item in name_list:
                            actor_names.append(item)
                    else:
                        actor_names.append(val)
                elif 'att&ck' in key.lower() and val:
                    attck_id = val
                elif 'target' in key.lower() and val:
                    target.append(val)
                elif 'operation' in key.lower() and val:
                    operations.append(val)
                elif 'operandi' in key.lower() and val:
                    description = val
                elif 'link' in key.lower() and val:
                    links.append(val)
                elif 'malware' in key.lower() and val:
                    if ',' in val:
                        tool_list = [x.strip() for x in val.split(',')]
                        for item in tool_list:
                            tools.append(item)
                    else:
                        tools.append(val)
                elif 'comment' in key.lower() and val:
                    comment = val
            
            if actor_names or target or operations or description or tools or links or attck_id or comment:
                self.generated_data.add_actor_item(
                    country=country,
                    names=actor_names,
                    targets=target,
                    operations=operations,
                    description=description,
                    tools=tools,
                    links=links,
                    attack_id=attck_id,
                    comment=comment
                )
            actor_names = []
            target = []
            operations = []
            description = None
            links = []
            tools = []
            attck_id = None
            comment = None
