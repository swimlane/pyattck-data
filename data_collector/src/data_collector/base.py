import abc

from requests import Session

from pyattck_data.attack import MitreAttck

from .logger import LoggingBase


class Base(metaclass=LoggingBase):

    attck: MitreAttck = None
    session: Session = Session()
    ENTERPRISE_ATTCK_JSON: dict = {}
