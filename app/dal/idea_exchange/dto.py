from dataclasses import dataclass
from datetime import datetime

from app.domain.auth.core import UserID, GroupID
from app.domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID
from app.framework.domain.abs import IDTO


@dataclass
class IdeaDalDto(IDTO):
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
class ChainDalDto(IDTO):
    chain_id: ChainID
    author_id: UserID
    reject_chain_link_id: ChainLinkID
    accept_chain_link_id: ChainLinkID
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class ActorDalDto(IDTO):
    actor_id: ActorID
    name: str
    groups_ids: list[GroupID]
    manager_ids: list[UserID]


@dataclass
class ChainLinkDalDto(IDTO):
    chain_link_id: ChainLinkID
    actor_id: ActorID
    name: str
    is_technical: bool
    order: int
    chain_id: ChainID
    number_of_related_ideas: int
    is_deleted: bool
