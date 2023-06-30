"""Contains helper functions for data_collector module."""
from typing import Any

from pyattck_data.technique import Technique

from .base import Base


class Helper(Base):

    def get_object_by_external_id(self, external_id: str, object_type: str) -> Any:
        """Returns a object from the pyattck_data library.

        Args:
            external_id (str): The external_id we are retrieving.

        Returns:
            Any: The Any object.
        """
        for item in self.attck.objects:
            if item.type == object_type:
                if item.external_references:
                    for ref in item.external_references:
                        if hasattr(ref, 'external_id') and ref.external_id == external_id:
                            return item
                        
    def get_object_by_name_or_aliases(self, name: str, object_type: str) -> Any:
        """Returns a object from the pyattck_data library.

        Args:
            name (str): The name or alias to search for.

        Returns:
            Any: The Any object.
        """
        for item in self.attck.objects:
            if item.type == object_type:
                if name in item.name:
                    return item
                if hasattr(item, 'aliases'):
                    if name in item.aliases:
                        return item
                if hasattr(item, "names"):
                    if name in item.names:
                        return item

    def replace_object(self, object: Any) -> None:
        """Replaces an object in the Enterprise Attack data object.

        Args:
            object (Any): An object to update
        """
        for index, item in enumerate(self.attck.objects):
            if item.type == object.type:
                if item.id == object.id:
                    self.attck.objects[index] = object
                    return
        raise Exception(f"Unable to find object to replace. {object}")