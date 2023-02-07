from datetime import datetime
from typing import Optional, Any, Callable
from dataclasses import dataclass


class ValueFromStorage:

    def __init__(self, val):
        pass

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass

    def __delete__(self, instance):
        pass


@dataclass
class BaseMeta:
    id_from_storage: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = None
    is_deleted: bool = False
    is_changed: bool = False


class MetaManipulation:

    _meta: BaseMeta

    def update_meta(self, new_meta: BaseMeta):
        self._meta = new_meta

    def replace_id_from_meta(self):
        raise NotImplementedError()
