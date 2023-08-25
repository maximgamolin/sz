from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class BaseMeta:
    """
    Дополнительная информация из хранилища, помещаемая в сущность
    """
    id_from_storage: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = None
    is_deleted: bool = False
    is_changed: bool = False


class MetaManipulation:
    """
    Класс отвечающий за работу с доп информацией из хранилища, находящейся в сущности/агрегате
    """

    _meta: BaseMeta

    def update_meta(self, new_meta: BaseMeta):
        """
        Обновить метаинформацию
        :param new_meta:
        :return:
        """
        self._meta = new_meta

    def replace_id_from_meta(self):
        raise NotImplementedError()
