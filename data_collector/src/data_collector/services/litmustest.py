from ..githubcontroller import GitHubController
from .base import Base


class LitmusTest(GitHubController, Base):
    """ Data Source: https://github.com/Kirtar22/Litmus_Test
    Authors:
        - Kirtar22

    This class is a wrapper for the above data set
    """
    
    URL = 'https://raw.githubusercontent.com/Kirtar22/Litmus_Test/master/{}'
    REPO = 'Kirtar22/Litmus_Test'

    def parse(self):
        self.count = 0
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('.md') and file_content.path.split('/')[-1].startswith('T'):
                    content = self.__download_raw_content(file_content.download_url)
                    self.__parse_markdown(content.decode('utf-8'))
        self.__logger.info(f"Added {self.count} commands from {self.REPO}")

    def __parse_markdown(self, content):
        if content.strip():
            template_id = False
            commands = False
            data_sources = False
            queries = False
            for line in content.splitlines():
                if not template_id:
                    if line.startswith('# '):
                        if line.strip('# ').split('-')[0].startswith('T'):
                            template_id = line.strip('# ').split('-')[0].strip()
                if '## Simulating the attack' in line:
                    commands = True
                    continue
                if commands:
                    if line:
                        if not line.startswith('#'):
                            technique = self.helper.get_object_by_external_id(template_id, "attack-pattern")
                            if technique:
                                technique.command_list.append(line.strip())
                                self.helper.replace_object(technique)
                                self.count += 1
                        elif line.startswith('#'):
                            commands = False
                if '## Data sources' in line:
                    data_sources = True
                    continue
                if data_sources:
                    if line:
                        if not line.startswith('#'):
                            technique = self.helper.get_object_by_external_id(template_id, "attack-pattern")
                            if technique:
                                technique.command_list.append(line.strip())
                                self.helper.replace_object(technique)
                                self.count += 1
                        elif line.startswith('#'):
                            data_sources = False
                if '## Splunk Queries' in line:
                    queries = True
                    continue
                if queries:
                    if line:
                        if line.startswith('###'):
                            continue
                        if not line.startswith('#'):
                            technique = self.helper.get_object_by_external_id(template_id, "attack-pattern")
                            if technique:
                                technique.command_list.append(line.strip())
                                self.helper.replace_object(technique)
                                self.count += 1
                        elif line.startswith('#'):
                            queries = False

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            return response.content
