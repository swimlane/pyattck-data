from datetime import datetime
from hashlib import new
from typing import AnyStr, List

from attrs import define, field
from pydantic import HttpUrl


@define
class Query:
    product: AnyStr = field()
    query: AnyStr = field()
    name: AnyStr = field()


@define
class TechniqueCommand:
    command: AnyStr = field()
    source: HttpUrl = field()
    name: AnyStr = field(factory=str)


@define
class Technique:
    technique_id: AnyStr = field()
    command_list: list = field(factory=list)
    commands: List[TechniqueCommand] = field(factory=list)
    parsed_datasets: list = field(factory=list)
    queries: List[Query] = field(factory=list)
    possible_detections: list = field(factory=list)
    external_reference: list = field(factory=list)

    def __attrs_post_init__(self):
        if self.commands:
            return_list = []
            for item in self.commands:
                if not isinstance(item, TechniqueCommand):
                    return_list.append(TechniqueCommand(**item))
                else: return_list.append(item)
            self.commands = return_list
        if self.queries:
            return_list = []
            for item in self.queries:
                if not isinstance(item, Query):
                    return_list.append(Query(**item))
                else: return_list.append(item)
            self.queries = return_list


@define
class C2Data:
    name: AnyStr = field(factory=str)
    license: AnyStr = field(factory=str)
    price: AnyStr = field(factory=str)
    github: AnyStr = field(factory=str)
    site: AnyStr = field(factory=str)
    twitter: AnyStr = field(factory=str)
    evaluator: AnyStr = field(factory=str)
    date: AnyStr = field(factory=str)
    version: int = field(factory=int)
    implementation: AnyStr = field(factory=str)
    how_to: AnyStr = field(factory=str)
    slingshot: AnyStr = field(factory=str)
    kali: AnyStr = field(factory=str)
    server: AnyStr = field(factory=str)
    socks_support: bool = field(factory=bool)
    implant: AnyStr = field(factory=str)
    multi_user: bool = field(factory=bool)
    ui: bool = field(factory=bool)
    dark_mode: bool = field(factory=bool)
    api: bool = field(factory=bool)
    windows: bool = field(factory=bool)
    linux: bool = field(factory=bool)
    macos: bool = field(factory=bool)
    tcp: bool = field(factory=bool)
    http: bool = field(factory=bool)
    http2: bool = field(factory=bool)
    http3: bool = field(factory=bool)
    dns: bool = field(factory=bool)
    doh: bool = field(factory=bool)
    icmp: bool = field(factory=bool)
    ftp: bool = field(factory=bool)
    imap: bool = field(factory=bool)
    mapi: bool = field(factory=bool)
    smb: bool = field(factory=bool)
    ldap: bool = field(factory=bool)
    key_exchange: bool = field(factory=bool)
    stego: bool = field(factory=bool)
    proxy_aware: bool = field(factory=bool)
    domainfront: bool = field(factory=bool)
    custom_profile: bool = field(factory=bool)
    jitter: bool = field(factory=bool)
    working_hours: bool = field(factory=bool)
    kill_date: bool = field(factory=bool)
    chaining: bool = field(factory=bool)
    logging: bool = field(factory=bool)
    in_wild: bool = field(factory=bool)
    attck_mapping: bool = field(factory=bool)
    dashboard: bool = field(factory=bool)
    blog: AnyStr = field(factory=str)
    c2_matrix_indicators: AnyStr = field(factory=str)
    jarm: bool = field(factory=bool)
    actively_maint: bool = field(factory=bool)
    slack: bool = field(factory=bool)
    slack_members: bool = field(factory=bool)
    gh_issues: bool = field(factory=bool)
    notes: AnyStr = field(factory=str)


@define
class Tool:
    names: list = field()
    comments: AnyStr = field()
    family: list = field(factory=list)
    links: list = field(factory=list)


@define
class Actor:
    country: AnyStr = field()
    names: List = field()
    targets: AnyStr = field()
    operations: List = field()
    description: AnyStr = field()
    external_tools: List = field()
    links: List = field()
    attck_id: AnyStr = field()
    comment: AnyStr = field()


@define
class GeneratedData:
    last_updated: datetime = field()
    techniques: List[Technique] = field(factory=list)
    c2_data: List[C2Data] = field(factory=list)
    tools: List[Tool] = field(factory=list)
    actors: List[Actor] = field(factory=list)

    def __attrs_post_init__(self):
        if self.techniques:
            return_list = []
            for item in self.techniques:
                return_list.append(Technique(**item))
            self.techniques = return_list
        if self.c2_data:
            return_list = []
            for item in self.c2_data:
                return_list.append(C2Data(**item))
            self.c2_data = return_list
        if self.tools:
            return_list = []
            for item in self.tools:
                return_list.append(Tool(**item))
            self.tools = return_list
        if self.actors:
            return_list = []
            for item in self.actors:
                return_list.append(Actor(**item))
            self.actors = return_list

    @last_updated.default
    def default_updated(self):
        return str(datetime.now())

    def add_actor_item(self, country, names, targets, operations, description, external_tools, links, attck_id, comment):
        self.actors.append(
            Actor(
                country=country,
                names=list(set(names)) if names else [],
                targets=list(set(targets)) if targets else [],
                operations=list(set(operations)) if operations else [],
                description=description,
                external_tools=list(set(external_tools)) if external_tools else [],
                links=list(set(links)) if links else [],
                attck_id=attck_id,
                comment=comment
            )
        )

    def add_tool_item(self, names, comments, family, links):
        tool = Tool(
            names=list(set(names)),
            comments=comments,
            family=family,
            links=list(set(links))
        )
        if self.tools:
            if tool not in self.tools:
                self.tools.append(tool)
        else:
            self.tools.append(tool)

    def add_command(self, technique_id, source, name, command):
        c = TechniqueCommand(
            command=command,
            source=source,
            name=name
        )
        if self.techniques:
            found = False
            for technique in self.techniques:
                if technique.technique_id == technique_id:
                    found = True
                    if technique.commands:
                        if c not in technique.commands:
                            technique.commands.append(c)
                    else:
                        technique.commands.append(c)

                    if technique.command_list:
                        if command not in technique.command_list:
                            technique.command_list.append(command)
                    else:
                        technique.command_list.append(command)
            if not found:
                self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        commands=[c],
                        command_list=[command]
                    )
                )
        else:
            self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        commands=[c],
                        command_list=[command]
                    )
                )

    def add_dataset(self, technique_id, content):
        if self.techniques:
            found = False
            for technique in self.techniques:
                if technique.technique_id == technique_id:
                    found = True
                    technique.parsed_datasets.append(content)
            if not found:
                self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        parsed_datasets=[content]
                    )
                )
        else:
            self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        parsed_datasets=[content]
                    )
                )

    def add_possible_queries(self, technique_id, product, content, name):
        q = Query(
            product=product,
            query=content,
            name=name
        )
        if self.techniques:
            found = False
            for technique in self.techniques:
                if technique.technique_id == technique_id:
                    found = True
                    technique.queries.append(q)
            if not found:
                self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        queries=[q]
                    )
                )
        else:
            self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        queries=[q]
                    )
                )

    def add_possible_detection(self, technique_id, data):
        if self.techniques:
            found = False
            for technique in self.techniques:
                if technique.technique_id == technique_id:
                    found = True
                    technique.possible_detections.append(data)
            if not found:
                self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        possible_detections=[data]
                    )
                )
        else:
            self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        possible_detections=[data]
                    )
                )

    def add_external_reference(self, technique_id, reference):
        if self.techniques:
            found = False
            for technique in self.techniques:
                if technique.technique_id == technique_id:
                    found = True
                    if reference not in technique.external_reference:
                        technique.external_reference.append(reference)
            if not found:
                self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        external_reference=[reference]
                    )
                )
        else:
            self.techniques.append(
                    Technique(
                        technique_id=technique_id,
                        external_reference=[reference]
                    )
                )

    def add_c2_data(self, data):
        if isinstance(data, dict):
            new_dict = {}
            for key, val in data.items():
                if key == 'Actively Maint. <12 mo':
                    new_dict['actively_maint'] = val
                elif key == 'att&ck_mapping':
                    new_dict['attck_mapping'] = val
                else:
                    new_dict[key.replace(' ','_').replace('-', '_').replace('&','').lower()] = val
            data = C2Data(**new_dict)
            if data not in self.c2_data:
                self.c2_data.append(data)
