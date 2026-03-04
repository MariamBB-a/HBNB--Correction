# app/persistence/repository.py
from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class defining the repository interface"""

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Return first object with matching attribute, or None if not found"""
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of repository pattern"""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None

    def delete(self, obj_id):
        return self._storage.pop(obj_id, None)

    def get_by_attribute(self, attr_name, attr_value, all_matches=False):
        """
        Retrieve object(s) by attribute value.

        Parameters:
            attr_name (str): name of the attribute
            attr_value: value to match
            all_matches (bool): if True, return all matching objects as list

        Returns:
            Object if all_matches=False, or list of objects if all_matches=True
        """
        matches = [obj for obj in self._storage.values()
                   if getattr(obj, attr_name, None) == attr_value]
        if all_matches:
            return matches
        return matches[0] if matches else None
