import yaml

from ..githubcontroller import GitHubController
from .base import Base


class MitreStockpile(GitHubController, Base):
    """
    Data Source: https://github.com/mitre/stockpile
    Authors:
        - Mitre

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/mitre/stockpile/master/{}'
    REPO = 'mitre/stockpile'

    def parse(self):
        self.count = 0
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('yml') and not file_content.path.endswith('index.yaml'):
                    if 'data/adversaries' in file_content.path:
                        content = self.__download_raw_content(self.URL.format(file_content.path))
                        self.__parse_yaml_content(content, file_content.path)
                    if 'data/abilities' in file_content.path:
                        content = self.__download_raw_content(self.URL.format(file_content.path))
                        self.__parse_yaml_content(content, file_content.path)
        self.__logger.info(f"Added {self.count} commands from {self.REPO}")

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
                    technique = self.helper.get_object_by_external_id(item["technique"]["attack_id"], "attack-pattern")
                    if technique:
                        if isinstance(item['platforms'], dict):
                            new_item = self.gen_dict_extract('command', item)
                            if new_item:
                                for command in new_item:
                                    technique.command_list.append(command)
                                    self.count += 1
                        else:
                            technique.commands.append(item["platforms"])

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            try:
                return yaml.load(response.content, Loader=yaml.FullLoader)
            except:
                pass