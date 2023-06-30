#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re

from deep_translator import GoogleTranslator

from ..githubcontroller import GitHubController
from .base import Base


class ThreatHuntingBook(GitHubController, Base):
    """
    Data Source: https://github.com/12306Br0/Security-operation-book

    Authors:
        - 12306Bro

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/12306Br0/Security-operation-book/master/{}'
    REPO = '12306Br0/Security-operation-book'
    TERM_MAP = {
        "description": ["external_reference"],
        "test case": ["parsed_datasets"],
        "detection": ["possible_detections"],
        "traces": ["parsed_datasets"],
        "splunk": ["possible_detections"],
        "reference": ["external_reference"],
        "elastic": ["possible_detections"],
        
    }

    def parse(self):
        self.translator = GoogleTranslator(source='auto', target='en')
        return_list = []
        repo = self.github.get_repo(self.REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('.md') and file_content.path.split('/')[-1].startswith('T'):
                    content = self.__download_raw_content(file_content.download_url)
                   # try:
                    translated = self.translator.translate(content)
                    template = self.__parse_markdown(translated)
                    if template:
                        return_list.append(template)
                   # except:
                    #    pass
        return return_list

    def _parse_code_blocks(self, content, technique_id):
        regexp = re.compile(r"# *([^#]+)")
        found = re.findall(regexp, content)
        name = None
        type_name = None
        for item in found:
            print(item)
            input('press')
            if isinstance(item, tuple):
                for match in item:
                    stripped_match = match.rstrip('\r\n')
                    if stripped_match:
                        for line in stripped_match.splitlines():
                            if line.startswith('## '):
                                if 'test' in line:
                                    name = line.strip('## ').strip()
                                    break
                                if 'detection rules' in line:
                                    name = line.strip('## ').strip()
                                    break
                        if name and name not in stripped_match:
                            if 'test' in name:
                                for line in stripped_match.splitlines():
                                    type_name = line
                                    break
                                if type_name:
                                    print(type_name)
                                    print(item)
                                    input('press')
                                    self.generated_data.add_command(
                                        technique_id=technique_id,
                                        source=self.__URL,
                                        name=type_name,
                                        command=stripped_match
                                    )
                                else:
                                    self.generated_data.add_command(
                                        technique_id=technique_id,
                                        source=self.__URL,
                                        name='',
                                        command=stripped_match
                                    )
                            if 'detection rules' in name:
                                for line in stripped_match.splitlines():
                                    type_name = line
                                    break
                                if type_name:
                                    self.generated_data.add_possible_queries(
                                        technique_id=technique_id,
                                        product=self.__URL,
                                        content=stripped_match,
                                        name=type_name
                                    )
                                else:
                                    self.generated_data.add_command(
                                        technique_id=technique_id,
                                        source=self.__URL,
                                        name='',
                                        command=stripped_match
                                    )

    def __parse_markdown(self, content):
        technique_id = None
        if content.strip():
            if not technique_id:
                for line in content.splitlines():
                    if line.strip().startswith('# T'):
                        technique_id = line.strip().split('-')[0].replace('#','').strip()
                        print(technique_id)
                        break
        if technique_id and content.strip():
            regexp = re.compile(r"## *([^#]+)")
            found = re.findall(regexp, content.strip())
            if found:
                next_item = False
                for item in found:
                    if next_item:
                        next_item = False
                        continue
                    title = None
                    data = None
                    if title and not data:
                        data = item.split(title)[-1].strip()
                        print(data)
                        input('press')
                    for line in item.strip():
                        if line:
                            for key,val in self.TERM_MAP.items():
                                if key.lower() in line.lower():
                                    if not title:
                                        title = line
                                   
                                    for v in val:
                                        print(v)
    
            # for line in content.splitlines():
            #     if line.startswith('# ') and not technique_id:
            #         line = line.split('# ')[-1].strip()
            #         if line.startswith('T'):
            #             technique_id = line.split('-')[0].strip()
            #             break
            #     elif line.startswith("## ") and technique_id:
            #         self._parse_code_blocks(content, technique_id)


    def __download_raw_content(self, url):
        response = self.session.get(url.encode('utf-8'))
        if response.status_code == 200:
            return response.text