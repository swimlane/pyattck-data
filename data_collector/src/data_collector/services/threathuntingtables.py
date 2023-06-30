import csv

from .base import Base


class ThreatHuntingTables(Base):
    """
    Data Source: https://github.com/dwestgard/threat_hunting_tables

    Authors:
        - dwestgard

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/dwestgard/threat_hunting_tables/master/process_chains.csv'

    def __get_csv_data(self):
        return_list = []
        response = self.session.get(self.URL)
        decoded_content = response.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        headers = my_list[0]
        for row in my_list:
            return_list.append(dict(zip(headers, row)))
        return return_list

    def int_or_float(self, strg):
        val = float(strg)
        return int(val) if val.is_integer() else val

    def get(self):
        for item in self.__get_csv_data():
            if item['mitre_attack'].startswith('T'):
                print(item)
                if item['parent_process']:
                    if item['commandline_string']:

                        self.generated_data.add_command(
                            technique_id=item["mitre_attack"],
                            source="Threat Hunting Tables",
                            name='',
                            command=f"{item['parent_process']} {item['commandline_string']}"
                        )
                    else:
                        self.generated_data.add_command(
                            technique_id=item["mitre_attack"],
                            source="Threat Hunting Tables",
                            name="parent_process",
                            command=item['parent_process']
                        )
                for key in ["file_path", "registry_path", "registry_value", "loaded_dll", "sub_process_1", "sub_process_2"]:
                    if item.get(key):
                        
                        self.generated_data.add_command(
                            technique_id=item["mitre_attack"],
                            source="Threat Hunting Tables",
                            command=item[key],
                            name=key
                        )
                self.generated_data.add_dataset(
                    technique_id=item["mitre_attack"],
                    content=item
                )
