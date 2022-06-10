import requests, xlrd

from ..base import Base


class AdversaryEmulation(Base):
    """
    Data Source: https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx
    Author: Mitre

    This class is a wrapper for the above data set
    """

    URL = 'https://attack.mitre.org/docs/APT3_Adversary_Emulation_Field_Manual.xlsx'

    OFFSET = 2
    
    def _parse(self, sheet):
        header_row = sheet.row(1)

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

        for item in rows:
            new_dict = {}
            if item['Category']:
                techniques = [s.strip() for s in item['Category'].splitlines()]

                if len(techniques) > 1:
                    for tech in techniques:
                        new_dict = {}
                        new_dict['Category'] = tech
                        for key, val in item.items():
                            if 'Category' != key:
                                new_dict[key] = val
                        
                        rows.append(new_dict)
                    rows.remove(item)
        return rows


    def __format(self, data):
        for item in data:
            if item['Built-in Windows Command']:
                self.generated_data.add_command(
                    technique_id=item["Category"],
                    command=item['Built-in Windows Command'],
                    source=self.URL,
                    name='Built-in Windows Command'
                )
            if item['Cobalt Strike']:
                self.generated_data.add_command(
                    technique_id=item["Category"],
                    source=self.URL, 
                    name='Cobalt Strike',
                    command=item["Cobalt Strike"]
                )
            if item['Metasploit']:
                self.generated_data.add_command(
                    technique_id=item["Category"],
                    source=self.URL,
                    name='Metasploit',
                    command=item['Metasploit']
                )
            self.generated_data.add_dataset(
                technique_id=item["Category"],
                content=item
            )
           
    def get(self):
        response = requests.get(self.URL)
        workbook = xlrd.open_workbook(file_contents=response.content)  # open workbook
        worksheet = workbook.sheet_by_index(0)  # get first sheet
        parsed_data = self._parse(worksheet)
        return self.__format(parsed_data)