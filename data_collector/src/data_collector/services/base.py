"""Base for all services. All services should inherit from this class."""
from abc import abstractmethod

from ..base import Base as BaseBase
from ..helper import Helper


class Base(BaseBase):
    """Base for all services. All services should inherit from this class."""

    URL: str = None
    helper = Helper()

    def scrape(self):
        """Scrape the data source."""
        self._set_response()
        self.parse()

    @abstractmethod
    def parse(cls):
        """Parse the data source."""
        raise NotImplementedError('parse method not implemented')

    def _set_response(self):
        self.response = self.session.get(self.URL)
