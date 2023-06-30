import yaml

from ..githubcontroller import GitHubController
from .base import Base


class ElementalAttack(GitHubController, Base):
    """
    Data Source: https://github.com/Elemental-attack/Elemental
    Author: 
        * Josh Hakala (<a href="https://github.com/exec-bypass">exec-bypass</a>)
        * Steve Rice (<a href="https://github.com/sdrice">sdrice</a>)
        * Aaron Crouch (<a href="https://github.com/TTwoONEsiXX">TTwoONEsiXX</a>)
        * Erick Pasco (<a href="https://github.com/epasco5">epasco5</a>)

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/Elemental-attack/Elemental/master/{}'
    REPO = 'Elemental-attack/Elemental'

    def parse(self):
        self.count = 0
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('yml'):
                    if 'sigma_rules/' in file_content.path:
                        content = self.__download_content(self.URL.format(file_content.path))
                        self.__get_attack_template(content)

    def __get_attack_template(self, return_list):
        for item in return_list:
            if item.get("title"):
                actor = self.helper.get_object_by_name_or_aliases(item.get("title"), "intrusion-set")
                if actor:
                    actor.external_description.append(item.get("description"))
                    if item.get("references"):
                        for ref in item.get("references"):
                            self.count += 1
                            actor.external_references.append({
                                "source_name": self.REPO,
                                "url": ref,
                                "external_id": item.get("id")
                            })
                    self.helper.replace_object(actor)
                else:
                    if item.get("tags"):
                        for tag in item.get("tags"):
                            if "attack." in tag:
                                tech_id = tag.split("attack.")[1]
                                technique = self.helper.get_object_by_external_id(tech_id.upper(), "attack-pattern")
                                if technique:
                                    if item.get("references"):
                                        technique.external_reference.extend(item.get("references"))
                                    technique.possible_detections.append(item.get("logsource"))
                                    technique.possible_detections.append(item.get("detection"))
                                    self.helper.replace_object(technique)
                                    self.count += 1
        self.__logger.debug(f"Processed {self.count} actors")

    def __download_content(self, url):
        return_list = []
        response = self.session.get(url)
        if response.status_code == 200:
            content = response.text
            if content:
                if '---' in content:
                    content = content.split('---')
                    for item in content:
                        return_list.append(yaml.load(item, Loader=yaml.FullLoader))
                else:
                    return_list.append(yaml.load(content, Loader=yaml.FullLoader))
        return return_list