from ..githubcontroller import GitHubController
from .base import Base


class OsqueryAttack(GitHubController, Base):
    """
    Data Source: https://github.com/teoseller/osquery-attck
    Authors:
        - teoseller

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/teoseller/osquery-attck/master/{}'
    REPO = 'teoseller/osquery-attck'

    def parse(self):
        self.count = 0
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('conf'):
                    self.__download_raw_content(self.URL.format(file_content.path))
        self.__logger.info(f"Added {self.count} queries from {self.REPO}")

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            content = response.json()
            if content.get('description'):
                technique_list = content["description"].split('ATT&CK: ')[-1].split(',')
                for key,val in content['queries'].items():
                    if len(technique_list) <= 2:
                        continue
                    else:
                        for technique in technique_list:
                            tech = self.helper.get_object_by_external_id(technique, "attack-pattern")
                            if tech:
                                self.count += 1
                                for k,v in val.items():
                                    if 'query' in k:
                                        tech.queries.append(v)
                                        self.count += 1
                                self.helper.replace_object(tech)
