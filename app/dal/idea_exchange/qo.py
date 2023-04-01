from dataclasses import dataclass
from typing import Optional, Union

from domain.auth.core import UserID
from domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID
from framework.data_access_layer.query_object.base import ABSQueryObject
from framework.data_access_layer.query_object.values import QueryParamComparison
from framework.data_access_layer.values import Empty


@dataclass
class IdeaQO(ABSQueryObject):
    name: Optional[Union[str, Empty, QueryParamComparison]] = Empty()
    chain_id: Optional[Union[ChainID, Empty, QueryParamComparison]] = Empty()
    idea_id: Optional[Union[IdeaID, Empty, QueryParamComparison]] = Empty()
    author_id: Optional[Union[UserID, Empty, QueryParamComparison]] = Empty()
    current_chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison]] = Empty()
    is_deleted: Optional[Union[bool, Empty, QueryParamComparison]] = Empty()


@dataclass
class ChainQO(ABSQueryObject):
    chain_id: Optional[Union[ChainID, Empty, QueryParamComparison]] = Empty()
    author_id: Optional[Union[UserID, Empty, QueryParamComparison]] = Empty()
    reject_chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison]] = Empty()
    accept_chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison]] = Empty()
    is_deleted: Optional[Union[bool, Empty, QueryParamComparison]] = Empty()


@dataclass
class ChainLinkQO(ABSQueryObject):
    chain_id: Optional[Union[ChainID, Empty, QueryParamComparison]] = Empty()
    is_technical: Optional[Union[bool, Empty, QueryParamComparison]] = Empty()
    actor_id: Optional[Union[ActorID, Empty, QueryParamComparison]] = Empty()
    is_deleted: Optional[Union[bool, Empty, QueryParamComparison]] = Empty()


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