from enum import IntEnum
from typing import Type, Optional, Iterable
from domain.idea_exchange.types import ChainID, IdeaID, ChainLinkID, ActorID
from dataclasses import dataclass
from exceptions.idea_exchange import ChainLinkNotInChain, NoChainLinksInChain, IncorrectChainLink
from domain.auth.core import User, Group
from framework.data_logic_layer.meta import BaseMeta, MetaManipulation


@dataclass
class IdeaAuthor(User):

    def can_delete_idea(self, idea: 'Idea'):
        return idea.author == self

    def can_edit_idea(self, idea: 'Idea'):
        return idea.author == self


@dataclass
class Manager(User):
    pass


@dataclass
class ChainEditor(User):
    pass


@dataclass
class Actor(MetaManipulation):
    actor_id: ActorID
    users: list[User]
    groups: list[Group]
    name: str

    def replace_id_from_meta(self):
        self.actor_id = self._meta.id_from_storage


class ChainLink(MetaManipulation):

    ACCEPT = "Одобрено"
    REJECT = "Отклонено"

    __slots__ = (
        'chain_link_id', 'actor',
        '_meta', 'name', 'is_technical',
        'number_of_related_ideas'
    )

    @dataclass
    class Meta(BaseMeta):
        is_technical: bool = False

    def __init__(
            self,
            chain_link_id: Optional[ChainLinkID],
            actor: Optional[Actor],
            name: str,
            number_of_related_ideas: int,
            is_technical: bool = False,
            _meta_is_deleted: bool = False,
            _meta_is_changed: bool = False,
    ):
        self.chain_link_id = chain_link_id
        self.actor = actor
        self.name = name
        self.is_technical = is_technical
        # Вообще, можно словить гонку, надо по ходу версию добавлять, для оптимистичной блокировки
        self.number_of_related_ideas = number_of_related_ideas
        self._meta: ChainLink.Meta = ChainLink.Meta(
            is_changed=_meta_is_changed,
            is_deleted=_meta_is_deleted
        )

    def __eq__(self, other: 'ChainLink'):
        return (
            self.chain_link_id == other.chain_link_id and
            self.actor == other.actor and
            self.name == other.name
        )

    @classmethod
    def initialize_technical(cls, name: str) -> 'ChainLink':
        return cls(
            chain_link_id=None,
            actor=None,
            is_technical=True,
            name=name,
            _meta_is_changed=True,
        )

    def is_new(self):
        return self.chain_link_id is None

    def set_for_change(self):
        self._meta.is_changed = True

    def set_as_deleted(self):
        self._meta.is_deleted = True
        self._meta.is_changed = True

    def replace_id_from_meta(self):
        self.chain_link_id = self._meta.id_from_storage


class Chain(MetaManipulation):

    __slots__ = (
        'chain_id', 'chain_links',
        'author', '_meta',
        'reject_chain_link', 'accept_chain_link',
        'dropped_chain_links'
    )

    def __init__(
            self,
            chain_id: Optional[ChainID],
            chain_links: Iterable[ChainLink],
            author: ChainEditor,
            reject_chain_link: ChainLink,
            accept_chain_link: ChainLink,
            _meta_is_deleted: bool = False,
            _meta_is_changed: bool = False
    ):
        self.chain_id = chain_id
        self.chain_links = chain_links
        self.dropped_chain_links: list[ChainLink] = []
        self.author = author
        self.reject_chain_link = reject_chain_link
        self.accept_chain_link = accept_chain_link
        self._meta = BaseMeta(
            is_deleted=_meta_is_deleted,
            is_changed=_meta_is_changed
        )

    @classmethod
    def initialize_new(
            cls,
            author: ChainEditor,
            accept_chain_link: Optional[ChainLink] = None,
            reject_chain_link: Optional[ChainLink] = None
    ) -> 'Chain':
        return cls(
            chain_id=None,
            chain_links=[],
            author=author,
            _meta_is_changed=True,
            accept_chain_link=accept_chain_link or ChainLink.initialize_technical(ChainLink.ACCEPT),
            reject_chain_link=reject_chain_link or ChainLink.initialize_technical(ChainLink.REJECT)
        )

    def element_position(self, chain_link: ChainLink) -> int:
        for n, i in enumerate(self.chain_links, start=1):
            if i.chain_link_id == chain_link.chain_link_id:
                return n
        raise ChainLinkNotInChain()

    def first_chain_link(self) -> ChainLink:
        chain_links = list(self.chain_links)
        if len(chain_links) < 1:
            raise NoChainLinksInChain()
        return chain_links[0]

    def replace_id_from_meta(self):
        self.chain_id = self._meta.id_from_storage

    def validate_chain_links(self, chain_links: list[ChainLink]) -> None:
        chain_links_ids_in_chain = set(
            i.chain_link_id for i in self.chain_links if i.chain_link_id is not None
        )
        for chain_link in chain_links:
            if chain_link.chain_link_id is not None and \
                    chain_link.chain_link_id not in chain_links_ids_in_chain:
                raise IncorrectChainLink(
                    f"Звено {chain_link.chain_link_id}:{chain_link.name} не принадлежит этой цепочке"
                )

    def replace_chain_links(self, chain_links: list[ChainLink]) -> None:
        old_chain_links = list(self.chain_links)
        used_chain_links: set[ChainLinkID] = set()
        for chain_link in chain_links:
            if chain_link.is_new():
                chain_link.set_for_change()
            else:
                old_chain_link = next(
                    (i for i in old_chain_links if chain_link.chain_link_id == i.chain_link_id)
                )
                if old_chain_link is None:
                    # TODO добавить варнинг
                    # Вообще странно, это должно отлететь на валидации
                    continue
                if chain_link != old_chain_link:
                    chain_link.set_for_change()
                used_chain_links.add(old_chain_link.chain_link_id)
        self.chain_links = chain_links
        for old_chain_link in old_chain_links:
            if old_chain_link.chain_link_id not in used_chain_links:
                old_chain_link.set_as_deleted()
                self.dropped_chain_links.append(old_chain_link)


@dataclass
class BaseIdeaEvent:
    user: User
    comment: str
    award: int


@dataclass
class AcceptIdeaEvent(BaseIdeaEvent):
    pass


@dataclass
class RejectIdeaEvent(BaseIdeaEvent):
    pass


class Idea(MetaManipulation):

    __slots__ = (
        'author', 'body', 'chain', 'idea_id',
        'current_chain_link', '_meta'
    )

    FIRST_POSITION = 1

    def __init__(
            self,
            author: IdeaAuthor,
            body: str,
            chain: Chain,
            current_chain_link: ChainLink,
            idea_id: Optional[IdeaID] = None,
            _meta_is_deleted: bool = False,
            _meta_is_changed: bool = False
    ):
        self.author = author
        self.body = body
        self.chain = chain
        self.idea_id = idea_id
        self.current_chain_link = current_chain_link
        self._meta = BaseMeta(
            is_deleted=_meta_is_deleted,
            is_changed=_meta_is_changed
        )

    @classmethod
    def initialize_new_idea(
            cls, author: IdeaAuthor, body: str, chain: Chain
    ) -> 'Idea':
        idea = cls(
            body=body,
            author=author,
            chain=chain,
            current_chain_link=chain.first_chain_link()
        )
        idea._meta.is_changed = True
        idea._meta.is_deleted = False
        return idea

    def mark_deleted(self):
        self._meta.is_deleted = True
        self._meta.is_changed = True

    def is_editable(self):
        return self.chain.element_position(self.current_chain_link) == Idea.FIRST_POSITION

    def update(self, body: str):
        if self.body != body:
            self.body = body
            self._meta.is_changed = True

    def replace_id_from_meta(self):
        self.idea_id = self._meta.id_from_storage
