from dataclasses import dataclass
from typing import Optional


@dataclass
class ActorUserInputDTO:
    users_ids: list[int]
    groups_ids: list[int]
    name: str


@dataclass
class ChainLinkUserInputDTO:
    chain_link_id: Optional[int]
    actor: ActorUserInputDTO
    position_in_list: int
    name: str


@dataclass
class IdeaChanLinkUserDTO:
    name: str
    is_current: bool


@dataclass
class IdeaUserDTO:
    name: str
    body: str
    is_accepted: bool
    is_rejected: bool
    chain_links: list[IdeaChanLinkUserDTO]
