import requests, yaml

from ..base import Base


class SysmonHunter(Base):
    """
    Data Source: https://github.com/baronpan/SysmonHunter
    Authors:
        - baronpan

    This class is a wrapper for the above data set
    """
    
    __URL = 'https://raw.githubusercontent.com/baronpan/SysmonHunter/master/misc/attck.yaml'

    def __get_data(self):
        response = requests.get(self.__URL)
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

    def get(self):
        for key,val in self.__get_data().items():
            for item in val['query']:
                command_name = ''.join(self.gen_dict_extract('pattern', item))
                self.generated_data.add_command(
                    technique_id=key,
                    source=f"SysmonHunter - {val['name']}",
                    command=command_name,
                    name=''
                )
            self.generated_data.add_dataset(
                technique_id=key,
                content=val
            )
