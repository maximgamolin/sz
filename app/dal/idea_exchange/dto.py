from dataclasses import dataclass
from datetime import datetime

from domain.auth.core import UserID
from domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID


@dataclass
class IdeaDtoFromOrm:
    idea_id: IdeaID
    author_id: UserID
    name: str
    body: str
    chain_id: ChainID
    current_chain_link_id: ChainLinkID
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class ChainDtoFromOrm:
    chain_id: ChainID
    actor_id: ActorID
    author_id: UserID
    reject_chain_link: ChainLinkID
    accept_chain_link: ChainLinkID
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class ActorDtoFromOrm:
    actor_id: ActorID
    name: str
