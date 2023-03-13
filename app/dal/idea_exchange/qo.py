from dataclasses import dataclass
from typing import Optional, Union

from domain.auth.core import UserID
from domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID
from framework.data_access_layer.query_object import ABSQueryObject, Empty


@dataclass
class IdeaQO(ABSQueryObject):
    name: Optional[Union[str, Empty]] = Empty()
    chain_id: Optional[Union[ChainID, Empty]] = Empty()
    idea_id: Optional[Union[IdeaID, Empty]] = Empty()
    author_id: Optional[Union[UserID, Empty]] = Empty()
    current_chain_link_id: Optional[Union[ChainLinkID, Empty]] = Empty()
    is_deleted: Optional[Union[bool, Empty]] = Empty()


@dataclass
class ChainQO(ABSQueryObject):
    chain_id: Optional[Union[ChainID, Empty]] = Empty()
    author_id: Optional[Union[UserID, Empty]] = Empty()
    reject_chain_link_id: Optional[Union[ChainLinkID, Empty]] = Empty()
    accept_chain_link_id: Optional[Union[ChainLinkID, Empty]] = Empty()
    is_deleted: Optional[Union[bool, Empty]] = Empty()


@dataclass
class AuthorQO(ABSQueryObject):
    pass


@dataclass
class ChainEditorQO(ABSQueryObject):
    pass


@dataclass
class ManagerQO(ABSQueryObject):
    pass


@dataclass
class ManagerOO(ABSQueryObject):
    pass


@dataclass
class ActorQO(ABSQueryObject):
    actor_id: Optional[Union[ActorID, Empty]] = Empty()
    name: Optional[Union[str, Empty]] = Empty()