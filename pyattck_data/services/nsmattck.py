import requests

from ..githubcontroller import GitHubController
from ..markdowntable import MarkdownTable
from ..base import Base


class NSMAttck(GitHubController, Base):
    """
    Data Source: https://github.com/0xtf/nsm-attack
    Authors:
        - oxtf

    This class is a wrapper for the above data set
    """
    

    __URL = 'https://raw.githubusercontent.com/0xtf/nsm-attack/master/{}'
    __REPO = '0xtf/nsm-attack'

    def __init__(self):
        super(NSMAttck, self).__init__()
        self.session = requests.Session()
        self._dataset = []
        self.__temp_attack_paths = []

    def get(self):
        repo = self.github.get_repo(self.__REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                try:
                    contents.extend(repo.get_contents(file_content.path))
                except:
                    try:
                        contents.extend(repo.get_contents(file_content.path.encode('utf-8')))
                    except:
                        print('Can not encode or decode {type} in nsm-attack.  file_content.path is {val}'.format(type=type(file_content.path), val=file_content.path))
                        continue
            else:
                if file_content.path.endswith('.md') and file_content.path.split('/')[0].startswith('T'):
                    content = self.__download_raw_content(file_content.download_url)
                    self.__parse_markdown(content, file_content.path.split('/')[0])

    def __parse_markdown(self, content, technique_id):
        if content:
            for row in MarkdownTable(raw_content=content).rows():
                detection = dict(row)
                self.generated_data.add_possible_queries(
                    technique_id=technique_id,
                    product="Suricata (NSM)",
                    content=detection["Signature"],
                    name=f"{detection['Rules']} Rule"
                )
                self.generated_data.add_dataset(
                    technique_id=technique_id,
                    content=detection
                )

    def __download_raw_content(self, url):
        response = self.session.get(url.encode('utf-8'))
        if response.status_code == 200:
            return response.text