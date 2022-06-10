import re
from pydantic import BaseModel


# https://ihateregex.io/expr/semver/

PATTERNS = {
    'semversion': {
        'pattern': "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
        'examples': ['1.1.1', '0.1.2', '99.99.99']
    },
    'types': {
        'pattern': None,
        'examples': ['relationship', 'x-mitre-matrix', 'identity', 'marking-definition', 'course-of-action', 'malware', 'tool', 'intrusion-set', 'x-mitre-data-source', 'x-mitre-data-component', 'x-mitre-tactic', 'attack-pattern', 'bundle']
    },
    'reference': {
        'pattern': None,
        'examples': ['identity', 'marking-definition', 'course-of-action', 'malware', 'tool', 'intrusion-set', 'x-mitre-data-source', 'x-mitre-data-component', 'x-mitre-tactic', 'attack-pattern']
    },
    'domains': {
        'pattern': None,
        'examples': ['mobile-attack', 'enterprise-attack']
    },
    'platforms': {
        'pattern': None,
        'examples': ['Windows', 'Android', 'iOS', 'macOS', 'Azure AD', 'SaaS', 'Network', 'Google Workspace', 'PRE', 'Containers', 'IaaS', 'Linux', 'Office 365']
    },
    'relationship': {
        'pattern': None,
        'examples': ['revoked-by', 'subtechnique-of', 'uses', 'detects', 'mitigates','related-to']
    }
}


REGEXS = {
    'semversion': re.compile(PATTERNS['semversion']['pattern'])
}


class BaseCustomType(str):

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate


class SemVersion(BaseCustomType):

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern=PATTERNS['semversion']['pattern'],
            # some example postcodes
            examples=PATTERNS['semversion']['examples'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = REGEXS['semversion'].fullmatch(v.upper())
        if not m:
            raise ValueError('Invalid SemVersion format')
        return cls(f'{m.group(1)} {m.group(2)}')

    def __repr__(self):
        return f'SemVersion({super().__repr__()})'


class Id(BaseCustomType):

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            examples=PATTERNS['types']['examples'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if '--' in v:
            type,id = v.split('--')
        else:
            type = v
        if type not in PATTERNS['types']['examples']:
            raise ValueError('Invalid Id attribute.')
        return cls(v)

    def __repr__(self):
        return f'Id({super().__repr__()})'


class MitreDomain(BaseCustomType):

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            examples=PATTERNS['domains']['examples'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if v not in PATTERNS['domains']['examples']:
            raise ValueError('Invalid MitreDomain attribute.')
        return cls(v)

    def __repr__(self):
        return f'MitreDomain({super().__repr__()})'


class MitrePlatform(BaseCustomType):

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            examples=PATTERNS['platforms']['examples'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if v not in PATTERNS['platforms']['examples']:
            raise ValueError('Invalid MitrePlatform attribute.')
        return cls(v)

    def __repr__(self):
        return f'MitrePlatform({super().__repr__()})'


class MitreRelationship(BaseCustomType):

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            examples=PATTERNS['relationship']['examples'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if v not in PATTERNS['relationship']['examples']:
            raise ValueError('Invalid MitreRelationship attribute.')
        return cls(v)

    def __repr__(self):
        return f'MitreRelationship({super().__repr__()})'
