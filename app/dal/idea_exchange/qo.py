from dataclasses import dataclass
from typing import Optional, Union

from app.domain.auth.core import UserID
from app.domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID
from app.framework.data_access_layer.query_object.base import ABSQueryObject
from app.framework.data_access_layer.query_object.values import QueryParamComparison
from app.framework.data_access_layer.values import Empty


@dataclass
class IdeaQO(ABSQueryObject):
    name: Optional[Union[str, Empty, QueryParamComparison[str]]] = Empty()
    chain_id: Optional[Union[ChainID, Empty, QueryParamComparison[ChainID]]] = Empty()
    idea_id: Optional[Union[IdeaID, Empty, QueryParamComparison[IdeaID]]] = Empty()
    idea_uid: Optional[Union[str, Empty, QueryParamComparison[str]]] = Empty()
    author_id: Optional[Union[UserID, Empty, QueryParamComparison[UserID]]] = Empty()
    current_chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison[ChainLinkID]]] = Empty()
    is_deleted: Optional[Union[bool, Empty, QueryParamComparison[bool]]] = Empty()


@dataclass
class ChainQO(ABSQueryObject):
    chain_id: Optional[Union[ChainID, Empty, QueryParamComparison[ChainID]]] = Empty()
    author_id: Optional[Union[UserID, Empty, QueryParamComparison[UserID]]] = Empty()
    reject_chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison[ChainLinkID]]] = Empty()
    accept_chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison[ChainLinkID]]] = Empty()
    is_deleted: Optional[Union[bool, Empty, QueryParamComparison[bool]]] = Empty()


@dataclass
class ChainLinkQO(ABSQueryObject):
    chain_link_id: Optional[Union[ChainLinkID, Empty, QueryParamComparison[ChainLinkID]]] = Empty()
    chain_id: Optional[Union[ChainID, Empty, QueryParamComparison[ChainID]]] = Empty()
    is_technical: Optional[Union[bool, Empty, QueryParamComparison[bool]]] = Empty()
    actor_id: Optional[Union[ActorID, Empty, QueryParamComparison[ActorID]]] = Empty()
    is_deleted: Optional[Union[bool, Empty, QueryParamComparison[bool]]] = Empty()


@dataclass
class AuthorQO(ABSQueryObject):
    author_id: Optional[Union[UserID, Empty, QueryParamComparison[UserID]]] = Empty()


@dataclass
class ChainEditorQO(ABSQueryObject):
    pass


@dataclass
class ManagerQO(ABSQueryObject):
    user_id: Optional[Union[UserID, QueryParamComparison[UserID], Empty]] = Empty()


@dataclass
class ActorQO(ABSQueryObject):
    actor_id: Optional[Union[ActorID, Empty, QueryParamComparison[ActorID]]] = Empty()
    name: Optional[Union[str, Empty, QueryParamComparison[str]]] = Empty()