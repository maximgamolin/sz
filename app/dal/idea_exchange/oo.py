from dataclasses import dataclass
from typing import Optional, Union

from framework.data_access_layer.order_object.base import ABSOrderObject
from framework.data_access_layer.order_object.values import OrderParamComparison
from framework.data_access_layer.values import Empty


@dataclass
class IdeaOO(ABSOrderObject):
    created_at: Optional[Union[str, Empty, OrderParamComparison]] = Empty()


@dataclass
class ChainOO(ABSOrderObject):
    created_at: Optional[Union[str, Empty, OrderParamComparison]] = Empty()


@dataclass
class ActorOO(ABSOrderObject):
    created_at: Optional[Union[str, Empty, OrderParamComparison]] = Empty()


@dataclass
class ChainLinkOO(ABSOrderObject):
    created_at: Optional[Union[str, Empty, OrderParamComparison]] = Empty()
    order: Optional[Union[str, Empty, OrderParamComparison]] = Empty()
