import yaml

from ..githubcontroller import GitHubController
from .base import Base


class AtomicRedTeam(GitHubController, Base):
    """
    Data Source: https://github.com/redcanaryco/atomic-red-team
    Author: Red Canary

    This class is a wrapper for the above data set
    """
    
    URL = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/{}'
    REPO = 'redcanaryco/atomic-red-team'
    _replacement_strings = ["#{{{0}}}", "${{{0}}}", "#{0}", "${0}"]

    def _path_replacement(self, string, path):
        try:
            string = string.replace("$PathToAtomicsFolder", path)
        except:
            pass
        try:
            string = string.replace("PathToAtomicsFolder", path)
        except:
            pass
        return string

    def _replace_command_string(self, command: str, path: str, input_arguments: list = [], executor=None):
        if command:
            command = self._path_replacement(command, path)
            if input_arguments:
                for name, arg_dict in input_arguments.items():
                    if arg_dict.get("default"):
                        for string in self._replacement_strings:
                            try:
                                command = command.replace(str(string.format(name)), str(arg_dict.get("default")))
                            except Exception as e:
                                self.__logger.error(f"Error replacing string: {e}")
                                pass
        return self._path_replacement(command, path)

    def parse(self) -> None:
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('yaml') and not file_content.path.endswith('index.yaml'):
                    if 'atomics/' in file_content.path:
                        content = self.__download_raw_content(self.URL.format(file_content.path))
                        self.__parse_yaml_content(content, file_content.path)

    def __parse_yaml_content(self, content, url):
        if 'atomic_tests' in content:
            tech = self.helper.get_object_by_external_id(content["attack_technique"], "attack-pattern")
            for test in content['atomic_tests']:
                if 'executor' in test:
                    if 'command' in test['executor']:
                        if 'input_arguments' in test:
                            self.temp_command_string = None
                            self.temp_command_string = self._replace_command_string(
                                command=test['executor']['command'],
                                path="",
                                input_arguments=test['input_arguments'],
                                executor=test['executor']["name"]
                            )
                            if tech:
                                tech.command_list.append(self.temp_command_string)
                                self.helper.replace_object(tech)
                            self.temp_command_string = None
                        else:
                            if tech:
                                tech.command_list.append(test['executor']['command'])
                                self.helper.replace_object(tech)
            if tech:
                tech.parsed_datasets.append({
                    "source": url,
                    "name": f"Atomic Red Team Test - {content['display_name']}",
                    "content": content,
                })
                self.helper.replace_object(tech)

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            return yaml.load(response.content, Loader=yaml.FullLoader)