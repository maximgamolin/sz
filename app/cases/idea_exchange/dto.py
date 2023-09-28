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

    def to_dict(self):
        return {
            'chain_link_id': self.chain_link_id,
            'name': self.name,
            'is_current': self.is_current
        }


@dataclass
class IdeaUoDto:
    idea_id: int
    name: str
    body: str
    is_accepted: bool
    is_rejected: bool
    chain_links: list[IdeaChanLinkUoDto]
    idea_uid: str

    def to_dict(self):
        return {
            'idea_id': self.idea_id,
            'name': self.name,
            'body': self.body,
            'is_accepted': self.is_accepted,
            'is_rejected': self.is_rejected,
            'chain_links': [i.to_dict() for i in self.chain_links]
        }
