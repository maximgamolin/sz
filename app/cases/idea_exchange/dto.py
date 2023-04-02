from dataclasses import dataclass
from typing import Optional


@dataclass
class ActorUiDto:
    users_ids: list[int]
    groups_ids: list[int]
    name: str


@dataclass
class ChainLinkUiDto:
    chain_link_id: Optional[int]
    actor: ActorUiDto
    position_in_list: int
    name: str


@dataclass
class IdeaChanLinkUoDto:
    chain_link_id: int
    name: str
    is_current: bool


@dataclass
class IdeaUoDto:
    idea_id: int
    name: str
    body: str
    is_accepted: bool
    is_rejected: bool
    chain_links: list[IdeaChanLinkUoDto]
