import json
import re

import orjson
import yaml

from ..githubcontroller import GitHubController
from .base import Base


class AttckDatasources(GitHubController, Base):

    """
    Data Source: https://github.com/mitre-attack/attack-datasources
    Author: MITRE ATT&CK

    This class is a wrapper for the above data set
    """

    URL = 'https://raw.githubusercontent.com/mitre-attack/attack-datasources/main/{}'
    REPO = 'mitre-attack/attack-datasources'

    def parse(self) -> None:
        self.count = 0
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('techniques_to_relationships_mapping.yaml'):
                    content = self.__download_raw_content(self.URL.format(file_content.path))
                    self.__parse_yaml_content(content)

    def __parse_yaml_content(self, content):
        content = orjson.dumps(content).decode()
        content = json.loads(content)
        for item in content:
            if item:
                technique = self.helper.get_object_by_external_id(item.get("technique_id"), "attack-pattern")
                if technique:
                    detection_dict = {}
                    for key, val in item.items():
                        if val and val != 'None':
                            detection_dict[key] = val
                    if detection_dict:
                        technique.possible_detections.append(detection_dict)
                        if item.get("references"):
                            technique.external_reference.append(item["references"])
                            self.helper.replace_object(technique)
                            self.count += 1
        self.__logger.debug(f"Processed {self.count} techniques")

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            return yaml.load(response.content, Loader=yaml.FullLoader)
