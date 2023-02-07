from unittest import TestCase
from cases.idea_exchange.idea import IdeaCase
from domain.idea_exchange.main import Idea, Chain, IdeaAuthor, \
    ChainLink, Actor, ChainEditor
from domain.idea_exchange.types import ChainID, IdeaID, ChainLinkID
from tests.fakes.dll.uow import FakeUOW
from random import randrange
from exceptions.auth import PermissionDenied
from exceptions.idea_exchange import IdeaIsNotEdiatable
from tests.factories.idea_exchange import ActorFactory, ChainEditorFactory, \
    ChainLinkFactory, ChainFactory, IdeaAuthorFactory, IdeaFactory


class TestChain(TestCase):

    def test_assert_true(self):
        self.assertTrue(True)

    def setUp(self) -> None:
        self.chain_link1 = ChainLinkFactory.create_chain_link(
            actor=ActorFactory.create_actor()
        )
        self.chain_link2 = ChainLinkFactory.create_chain_link(
            actor=ActorFactory.create_actor()
        )
        self.reject_chain_link = ChainLinkFactory.create_chain_link(
            actor=ActorFactory.create_actor()
        )
        self.accept_chain_link = ChainLinkFactory.create_chain_link(
            actor=ActorFactory.create_actor()
        )
        self.chain_editor = ChainEditorFactory.create_chain_editor()
        self.chain = ChainFactory.create_chain(
            chain_links=[self.chain_link1, self.chain_link2],
            author=self.chain_editor,
            accept_chain_link=self.accept_chain_link,
            reject_chain_link=self.reject_chain_link
        )

    def test_add_all_new_chain_links(self):
        new_chain_link = ChainLinkFactory.create_chain_link(
            chain_link_id=None,
            actor=ActorFactory.create_actor()
        )
        another_chain_link = ChainLinkFactory.create_chain_link(
            chain_link_id=None,
            actor=ActorFactory.create_actor()
        )
        last_chain_link = ChainLinkFactory.create_chain_link(
            chain_link_id=None,
            actor=ActorFactory.create_actor()
        )
        self.chain.replace_chain_links(
            [new_chain_link, another_chain_link, last_chain_link]
        )
        self.assertEqual(3, len(list(self.chain.chain_links)))
        self.assertEqual(2, len(self.chain.dropped_chain_links))
        self.assertIn(new_chain_link, self.chain.chain_links)
        self.assertIn(another_chain_link, self.chain.chain_links)
        self.assertIn(last_chain_link, self.chain.chain_links)
        self.assertNotIn(self.chain_link1, self.chain.chain_links)
        self.assertNotIn(self.chain_link2, self.chain.chain_links)
        self.assertIn(self.chain_link1, self.chain.dropped_chain_links)
        self.assertIn(self.chain_link2, self.chain.dropped_chain_links)
        for i in self.chain.dropped_chain_links:
            self.assertTrue(i._meta.is_deleted)
            self.assertTrue(i._meta.is_changed)
