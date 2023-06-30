import yaml

from .base import Base


class SysmonHunter(Base):
    """
    Data Source: https://github.com/baronpan/SysmonHunter
    Authors:
        - baronpan

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/baronpan/SysmonHunter/master/misc/attck.yaml'

    def __get_data(self):
        response = self.session.get(self.URL)
        return yaml.load(response.content, Loader=yaml.FullLoader)

    def gen_dict_extract(self, key, var):
        if hasattr(var,'items'):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.gen_dict_extract(key, d):
                            yield result

    def parse(self):
        self.count = 0
        for key,val in self.__get_data().items():
            technique = self.helper.get_object_by_external_id(key, "attack-pattern")
            if technique:
                for item in val['query']:
                    command_name = ''.join(self.gen_dict_extract('pattern', item))
                    technique.command_list.append(command_name)
                    self.count += 1
                self.helper.replace_object(technique)
        self.__logger.info(f"Added {self.count} commands from {self.URL}")
