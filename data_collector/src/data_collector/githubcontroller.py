import yaml, os
from github import Github
from github import Auth

from .base import Base


class GitHubController(Base):

    def __init__(self):
        try:
            self.auth = Auth.Token(self.__get_token_from_env_variable())
        except:
            self.auth = Auth.Token(self.__get_token_from_config())
        self.github = Github(auth=self.auth)

    def __get_token_from_env_variable(self):
        if 'GH_TOKEN' in os.environ:
            return os.environ['GH_TOKEN']
        return ''

    def __get_token_from_config(self):
        cfg = ''
        with open("./config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        if 'GitHub' in cfg:
            if 'token' in cfg['GitHub']:
                return cfg['GitHub']['token']
