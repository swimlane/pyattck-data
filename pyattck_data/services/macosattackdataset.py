import requests, base64, json

from ..githubcontroller import GitHubController
from ..attacktemplate import AttackTemplate
from ..base import Base


class MacOSAttackDataset(GitHubController, Base):
    """
    Data Source: https://github.com/sbousseaden/macOS-ATTACK-DATASET
    Author: sbousseaden

    This class is a wrapper for the above data set
    """
    
    __RAW_URL = 'https://raw.githubusercontent.com/sbousseaden/macOS-ATTACK-DATASET/master/{}'
    __REPO = 'sbousseaden/macOS-ATTACK-DATASET'

    def __init__(self):
        super(MacOSAttackDataset, self).__init__()
        self.session = requests.Session()
        self._dataset = []

    def get(self):
        return_list = []
        repo = self.github.get_repo(self.__REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('json'):
                    #if 'atomics/' in file_content.path:
                    content = self.__download_raw_content(self.__RAW_URL.format(file_content.path))
                    return_list.append(self.__parse_json_content(content, file_content.path))
        
        return return_list
    
    def __parse_json_content(self, content, url):
        template = AttackTemplate()

        print(url)
        command_string = []
        for item in content:
            for key,val in item.items():
                if key == '_source':
                    executable = None
                    command_list = []
                    if val.get('process').get('executable'):
                        executable = val['process']['executable']
                    if val.get('process').get('args'):
                        if executable:
                            for ex in val['process']['args']:
                                if ex in executable:
                                    command_list.append(executable)
                                else:
                                    command_list.append(ex)
                            command_string.append(' '.join([x for x in command_list]))
        print(command_string)
              #  print(val)
        input('press')

    #    print(type(content))
    ##    print(content)
     #   input('press')
                        
    def __parse_yaml_content(self, content, url):
        template = AttackTemplate()
       # print(content)
        for test in content['atomic_tests']:
            if 'executor' in test:
                if 'command' in test['executor']:
                    if 'input_arguments' in test:
                        self.temp_command_string = None
                        for key,val in test['input_arguments'].items():
                            replacement_string = '#{{{0}}}'.format(key)
                            if self.temp_command_string is None:
                                try:
                                    self.temp_command_string = test['executor']['command'].replace(replacement_string, test['input_arguments'][key]['default'])
                                except:
                                    pass
                            else:
                                try:
                                    self.temp_command_string = self.temp_command_string.replace(replacement_string, test['input_arguments'][key]['default'])
                                except:
                                    pass
                            template.add_command(url,self.temp_command_string)
                            self.temp_command_string = None
                    else:
                        template.add_command(url,test['executor']['command'])
        template.id = content['attack_technique']
        template.add_dataset('Atomic Red Team Test - {name}'.format(name=content['display_name']), content)
        return template.get()      
        

    def bracketed_split(self, string, delimiter, strip_brackets=False):
        """ Split a string by the delimiter unless it is inside brackets.
            e.g.
            list(bracketed_split('abc,(def,ghi),jkl', delimiter=',')) == ['abc', '(def,ghi)', 'jkl']
        """
        openers = '[{(<'
        closers = ']})>'
        opener_to_closer = dict(zip(openers, closers))
        opening_bracket = dict()
        current_string = ''
        depth = 0
        for c in string:
            if c in openers:
                depth += 1
                opening_bracket[depth] = c
                if strip_brackets and depth == 1:
                    continue
            elif c in closers:
                assert depth > 0, f"You exited more brackets that we have entered in string {string}"
                assert c == opener_to_closer[opening_bracket[depth]], f"Closing bracket {c} did not match opening bracket {opening_bracket[depth]} in string {string}"
                depth -= 1
                if strip_brackets and depth == 0:
                    continue
            if depth == 0 and c == delimiter:
                yield current_string
                current_string = ''
            else:
                current_string += c
        assert depth == 0, f'You did not close all brackets in string {string}'
        yield current_string

    def __download_raw_content(self, url):
        return_list = []
        response = self.session.get(url)
        if response.status_code == 200:
            data = list(self.bracketed_split(response.content.decode(), '\n'))
            for item in data:
                if len(item) >= 1:
                    try:
                        return_list.append(json.loads(item))
                    except:
                        pass
        return return_list
