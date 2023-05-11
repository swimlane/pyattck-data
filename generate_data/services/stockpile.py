import requests, yaml

from ..githubcontroller import GitHubController
from ..base import Base


class MitreStockpile(GitHubController, Base):
    """
    Data Source: https://github.com/mitre/stockpile
    Authors:
        - Mitre

    This class is a wrapper for the above data set
    """
    
    __RAW_URL = 'https://raw.githubusercontent.com/mitre/stockpile/master/{}'
    __REPO = 'mitre/stockpile'

    def __init__(self):
        super(MitreStockpile, self).__init__()
        self.session = requests.Session()
        self._dataset = []
        self.__temp_attack_paths = []

    @property
    def stockpile(self):
        return self.__stockpile

    @stockpile.setter
    def stockpile(self, val):
        self.__stockpile = val

    @property
    def attack_paths(self):
        return self.__attack_paths

    @attack_paths.setter
    def attack_paths(self, val):
        self.__attack_paths = val


    def get_stockpile(self):
        return self.__stockpile

    def get_attack_paths(self):
        return self.__attack_paths

    def get(self):
        repo = self.github.get_repo(self.__REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('yml') and not file_content.path.endswith('index.yaml'):
                    if 'data/adversaries' in file_content.path:
                        content = self.__download_raw_content(self.__RAW_URL.format(file_content.path))
                        self.__parse_yaml_content(content, file_content.path)
                    if 'data/abilities' in file_content.path:
                        content = self.__download_raw_content(self.__RAW_URL.format(file_content.path))
                        self.__parse_yaml_content(content, file_content.path)

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
                        
    def __parse_yaml_content(self, content, url):
        if isinstance(content, list):
            for item in content:
                if item.get('platforms') and item.get("technique") and item.get("description"):
                    if isinstance(item['platforms'], dict):
                        new_item = self.gen_dict_extract('command', item)
                        if new_item:
                            for command in new_item:
                                self.generated_data.add_command(
                                    technique_id=item["technique"]["attack_id"],
                                    source=url,
                                    command=command,
                                    name=item["description"]
                                )
                    else:
                        self.generated_data.add_command(
                            technique_id=item["technique"]["attack_id"],
                            source=url,
                            command=item["platforms"],
                            name=item["description"]
                        )
                self.generated_data.add_dataset(
                    technique_id=item["technique"]["attack_id"],
                    content=item
                )
        else:
            if content:
                if 'phases' in content:
                    self.__temp_attack_paths.append(content)

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            try:
                return yaml.load(response.content, Loader=yaml.FullLoader)
            except:
                pass