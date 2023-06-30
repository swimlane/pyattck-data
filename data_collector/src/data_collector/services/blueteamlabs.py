from ..githubcontroller import GitHubController
from .base import Base


class BlueTeamLabs(GitHubController, Base):
    """ Data Source: https://github.com/BlueTeamLabs/sentinel-attack
    Authors:
        - [Edoardo Gerosa](https://twitter.com/netevert)
        - [Olaf Hartong](https://twitter.com/olafhartong) 

    This class is a wrapper for the above data set
    """
    
    URL = 'https://raw.githubusercontent.com/BlueTeamLabs/sentinel-attack/master/{}'
    REPO = 'BlueTeamLabs/sentinel-attack'

    def parse(self):
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('txt'):
                    if 'detections/' in file_content.path:
                        content = self.__download_raw_content(self.URL.format(file_content.path))
                        file_name = file_content.path.rsplit('/', 1)[1]
                        technique_id = file_name.split('_',1)[0]
                        tech = self.helper.get_object_by_external_id(technique_id, "attack-pattern")
                        if tech:
                            tech.queries.append(content)
                            self.helper.replace_object(tech)

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            lines = ''
            for line in response.text.splitlines():
                if not line.strip().startswith("//"):
                    lines += line
            return lines
