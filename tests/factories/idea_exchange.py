from random import randrange

from framework.test.utils import generate_random_string, Empty
from domain.idea_exchange.types import ChainLinkID, ActorID, ChainID, IdeaID
from domain.idea_exchange.main import Chain, ChainLink, Actor, ChainEditor,\
    IdeaAuthor, Idea


class ActorFactory:

    @staticmethod
    def create_actor(
            actor_id=Empty(),
            name=Empty(),
            users=Empty(),
            groups=Empty()
    ) -> Actor:
        return Actor(
            actor_id=actor_id if not isinstance(actor_id, Empty) else ActorID(randrange(1, 100)),
            name=name if not isinstance(name, Empty) else generate_random_string(10),
            users=users if not isinstance(users, Empty) else [],
            groups=groups if not isinstance(groups, Empty) else []
        )


class ChainLinkFactory:

    @staticmethod
    def create_chain_link(
            actor,
            chain_link_id=Empty(),
            name=Empty(),
            number_of_related_ideas=Empty()
    ) -> ChainLink:
        return ChainLink(
            chain_link_id=chain_link_id if not isinstance(chain_link_id, Empty) else ChainLinkID(randrange(1, 100)),
            actor=actor,
            name=name if not isinstance(name, Empty) else generate_random_string(10),
            number_of_related_ideas=number_of_related_ideas if not isinstance(number_of_related_ideas, Empty) else randrange(1, 100)
        )


class ChainEditorFactory:

    @staticmethod
    def create_chain_editor(
        user_id=Empty(),
    ) -> ChainEditor:
        return ChainEditor(
            user_id=user_id if not isinstance(user_id, Empty) else randrange(1, 100)
        )


class ChainFactory:

    @staticmethod
    def create_chain(
            author: ChainEditor,
            accept_chain_link: ChainLink,
            reject_chain_link: ChainLink,
            chain_id=Empty(),
            chain_links=Empty()
    ) -> Chain:
        return Chain(
            chain_links=chain_links if not isinstance(chain_links, Empty) else [],
            chain_id=chain_id if isinstance(chain_id, Empty) else ChainID(randrange(1, 100)),
            author=author,
            accept_chain_link=accept_chain_link,
            reject_chain_link=reject_chain_link
        )


class IdeaAuthorFactory:

    @staticmethod
    def create_idea_author(
            user_id=Empty(),
    ) -> IdeaAuthor:
        return IdeaAuthor(
            user_id=user_id if not isinstance(user_id, Empty) else randrange(1, 100)
        )


class IdeaFactory:

    @staticmethod
    def create_idea(
            author,
            chain,
            current_chain_link,
            idea_id=Empty(),
            body=Empty(),
            meta_is_changed=Empty(),
            meta_is_deleted=Empty()
    ) -> Idea:
        return Idea(
            idea_id=idea_id if not isinstance(idea_id, Empty) else IdeaID(randrange(1, 100)),
            author=author,
            body=body if not isinstance(body, Empty) else generate_random_string(10),
            chain=chain,
            current_chain_link=current_chain_link,
            _meta_is_changed=meta_is_changed if not isinstance(meta_is_changed, Empty) else False,
            _meta_is_deleted=meta_is_deleted if not isinstance(meta_is_deleted, Empty) else False,
        )
