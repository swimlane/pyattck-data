import openpyxl

from .base import Base


class AttckEmpire(Base):
    """
    Data Source: https://github.com/dstepanic/attck_empire
    Author: dstepanic

    This class is a wrapper for the above data set, which is focused on detection of 
    specific Empire modules related to ATT&CK Techniques.
    """

    URL = 'https://github.com/dstepanic/attck_empire/blob/master/Empire_modules.xlsx?raw=true'
    OFFSET = 1

    def parse(self):
        response = self.session.get(self.URL)
        open("Empire_modules.xlsx", "wb").write(response.content)
        workbook = openpyxl.load_workbook(
            filename="Empire_modules.xlsx"
        )
        columns = None
        for item in workbook["Empire_Modules"].values:
            if not columns:
                columns = item
            else:
                technique = item[1]
                tech = self.helper.get_object_by_external_id(technique, "attack-pattern")
                if tech:
                    tech.command_list.append(item[0])
                if item[2]:
                    tech = self.helper.get_object_by_external_id(item[2], "attack-pattern")
                    if tech:
                        tech.command_list.append(item[0])
                self.helper.replace_object(tech)
