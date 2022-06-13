import openpyxl
import requests

from ..base import Base


class AdversaryEmulation(Base):
    """
    Data Source: https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx
    Author: Mitre

    This class is a wrapper for the above data set
    """

    URL = 'https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx'

    OFFSET = 2

    def get(self):
        response = requests.get(self.URL)
        open('APT3_Adversary_Emulation_Field_Manual.xlsx', 'wb').write(response.content)
        workbook = openpyxl.load_workbook('APT3_Adversary_Emulation_Field_Manual.xlsx')
        return_dict = {}
        for item in workbook['Sheet1'].values:
            if item and item[0] and item[0].startswith('T'):
                for i in item[0].split():
                    if i not in return_dict:
                        return_dict[i] = {
                            "Built-in Windows Command": [],
                            "Cobalt Strike": [],
                            "Metasploit": [],
                            "Description": []
                        }
                    self.generated_data.add_command(
                        technique_id=i,
                        source=self.URL,
                        name="Built-in Windows Command",
                        command=item[1]
                    )
                    self.generated_data.add_command(
                        technique_id=i,
                        source=self.URL,
                        name="Cobalt Strike",
                        command=item[2]
                    )
                    self.generated_data.add_command(
                        technique_id=i,
                        source=self.URL,
                        name="Metasploit",
                        command=item[3]
                    )
                    self.generated_data.add_dataset(
                        technique_id=i,
                        content=item
                    )
