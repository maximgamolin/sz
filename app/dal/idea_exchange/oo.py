from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from framework.data_access_layer.query_object import ABSOrderObject, Empty


@dataclass
class IdeaOO(ABSOrderObject):
    created_at: Optional[Union[datetime, Empty]] = Empty()


@dataclass
class ChainOO(ABSOrderObject):
    pass
