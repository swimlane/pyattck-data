import csv

from .base import Base


class APTThreatTracking(Base):

    """
    Data Source: https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/edit#
    Author: Uknown

    This class is a wrapper for the above data set
    """

    URL = 'https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/export?format=csv&id=1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU&gid={gid}'

    GID_MAP  = {
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

    def parse(self) -> None:
        return_list = []
        for key,val in self.GID_MAP.items():
            if key != 'readme':
                response = self.session.get(self.URL.format(gid=val))
                data = response.text
                count = 0
                dict_list = []
                for item in csv.reader(data.splitlines()):
                    count += 1
                    if key == 'malware':
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
                        # Creates a map of headers to items
                        c2_dict = dict(zip(headers, item))
                        dict_list.append(c2_dict)

                if key not in ['malware', 'dll_side_loading', 'naming_schema', 'sources']:
                    self.__parse_data(key, dict_list=dict_list)
                else:
                    self.__parse_malware_tool_data(dict_list=dict_list)

    def __parse_malware_tool_data(self, dict_list):
        tool_names = []
        family_names = []
        comments = []
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
                    comments.append(val)
                elif 'link' in key.lower() and val:
                    links.append(val)
            if tool_names or family_names or comments or links:
                for name in tool_names:
                    tool = self.helper.get_object_by_external_id(name, "tool")
                    if tool:
                        if tool_names:
                            tool.names.extend(tool_names)
                        if family_names:
                            tool.family.extend(family_names)
                        if links:
                            tool.links.extend(links)
                        if comments:
                            tool.comment = comments
                        self.helper.replace_object(tool)
            tool_names = []
            family_names = []
            comments = []
            links = []

    def __parse_data(self, country, dict_list):
        actor_names = []
        target = []
        operations = []
        description = None
        links = []
        tools = []
        attck_id = None
        comments = []
        for item in dict_list:
            for key,val in item.items():
                if 'name' in key.lower() and val:
                    actor_names.append(val)
                elif key.lower() in ['crowdstrike','talos','dell', 'irl','kaspersky','secureworks','mandiant','fireeye','symantec','isight','cisco','palo','overlaps','mitre att&ck'] and val:
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
                    comments.append(val)
            
            if actor_names or target or operations or description or tools or links or attck_id or comments:
                for name in actor_names:
                    tech = self.helper.get_object_by_external_id(name, "intrusion-set")
                    if tech:
                        if actor_names:
                            tech.names.extend(actor_names)
                        if target:
                            tech.targets.extend(target)
                        if description:
                            tech.external_description.extend(description)
                        if tools:
                            tech.external_tools.extend(tools)
                        if links:
                            tech.links.extend(links)
                        if comments:
                            tech.comment = comments
                        self.helper.replace_object(tech)

            actor_names = []
            target = []
            operations = []
            description = None
            links = []
            tools = []
            attck_id = None
            comment = None
