import openpyxl
import requests

from ..base import Base


class AttckEmpire(Base):
    """
    Data Source: https://github.com/dstepanic/attck_empire
    Author: dstepanic

    This class is a wrapper for the above data set, which is focused on detection of 
    specific Empire modules related to ATT&CK Techniques.
    """

    URL = 'https://github.com/dstepanic/attck_empire/blob/master/Empire_modules.xlsx?raw=true'

    OFFSET = 1
    
    def _parse(self, sheet):
        header_row = sheet.row(0)

        columns = []
        for item in header_row:
            columns.append(str(item).split(':')[1].replace("'","").lstrip('u'))
    
        rows = []
        for i, row in enumerate(range(sheet.nrows)):
            if i <= self.OFFSET:
                continue
            r = []
            for j, col in enumerate(range(sheet.ncols)):
                r.append(sheet.cell_value(i, j))
            rows.append(dict(zip(columns, r)))
        return rows

    def __format(self, data):
        for item in data:
            if 'ATT&CK Technique #1' in item:
                if 'Empire Module' in item:
                    self.generated_data.add_command(
                        technique_id=item['ATT&CK Technique #1'],
                        source=self.URL,
                        name="Empire Module Command",
                        command=item["Empire Module"]
                    )
            if 'ATT&CK Technique #2' in item:
                if 'Empire Module' in item:
                    self.generated_data.add_command(
                        technique_id=item['ATT&CK Technique #1'],
                        source=self.URL,
                        name="Empire Module Command",
                        command=item["Empire Module"]
                    )
            self.generated_data.add_dataset(
                technique_id=item['ATT&CK Technique #1'],
                content=item
            )

    def get(self):
        response = requests.get(self.URL)
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
                self.generated_data.add_command(
                    technique_id=technique,
                    source=self.URL,
                    name="Empire Module Command",
                    command=item[0]
                )
                if item[2]:
                    self.generated_data.add_command(
                        technique_id=item[2],
                        source=self.URL,
                        name="Empire Module Command",
                        command=item[0]
                    )
                    self.generated_data.add_dataset(
                        technique_id=item[2],
                        content=item
                    )
                self.generated_data.add_dataset(
                    technique_id=technique,
                    content=item
                )
