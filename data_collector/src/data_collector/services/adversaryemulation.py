import openpyxl

from .base import Base


class AdversaryEmulation(Base):
    """
    Data Source: https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx
    Author: Mitre

    This class is a wrapper for the above data set
    """

    URL = 'https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx'
    OFFSET = 2

    def parse(self) -> None:
        self.count = 0
        response = self.session.get(self.URL)
        open('APT3_Adversary_Emulation_Field_Manual.xlsx', 'wb').write(response.content)
        workbook = openpyxl.load_workbook('APT3_Adversary_Emulation_Field_Manual.xlsx')
        for item in workbook['Sheet1'].values:
            if item and item[0] and item[0].startswith('T'):
                techniques = item[0].split()
                for t in techniques:
                    technique = self.helper.get_object_by_external_id(t, "attack-pattern")
                    for i in item[1:-1]:
                        if i:
                            technique.command_list.append(i)
                            self.count += 1
                    self.helper.replace_object(technique)
        self.__logger.info(f"Added {self.count} commands from {self.URL}")
