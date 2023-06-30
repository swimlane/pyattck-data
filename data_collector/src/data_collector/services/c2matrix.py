import csv

from .base import Base


class C2Matrix(Base):
    """
    Data Source: https://www.thec2matrix.com/
    Authors:
        - [Jorge Orchilles](https://twitter.com/jorgeorchilles)
        - [Bryson Bort](https://twitter.com/brysonbort) 
        - [Adam Mashinchi](https://twitter.com/adam_mashinchi)

    This class is a wrapper for the above data set, which is focused on details surrounding different C2 (Command & Control) tools/software
    """
    URL = 'https://docs.google.com/spreadsheet/ccc?key=1b4mUxa6cDQuTV2BPC6aA-GR4zGZi0ooPYtBe4IgPsSc&output=csv'
    OFFSET = 1

    def parse(self):
        response = self.session.get(self.URL)
        data = response.text
        self._parse(data)

    def _parse(self, data):
        obj_count = 0
        count = 0
        mal_count = 0
        headers = None
        for item in csv.reader(data.splitlines()):
            count += 1
            if count == 1:
                continue
            if count == 2:
                headers = item
                continue
            c2_dict = dict(zip(headers, item))
            tool = self.helper.get_object_by_name_or_aliases(c2_dict.get("Name"), "tool")
            malware = self.helper.get_object_by_name_or_aliases(c2_dict.get("Name"), "malware")
            if tool:
                for key,val in c2_dict.items():
                    if hasattr(tool, key):
                        setattr(tool, key, val)
                        obj_count += 1
                    if hasattr(tool, key.lower()):
                        setattr(tool, key.lower(), val)
                        obj_count += 1
                self.helper.replace_object(tool)
            if malware:
                for key,val in c2_dict.items():
                    if hasattr(malware, key):
                        setattr(malware, key, val)
                        mal_count += 1
                    if hasattr(malware, key.lower()):
                        setattr(malware, key.lower(), val)
                        mal_count += 1
                self.helper.replace_object(malware)
        self.__logger.debug(f"Processed {obj_count} C2 tools")
        self.__logger.debug(f"Processed {mal_count} C2 malware")
