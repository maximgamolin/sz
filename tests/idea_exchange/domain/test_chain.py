from unittest import TestCase
from cases.idea_exchange.idea import IdeaCase
from domain.idea_exchange.main import Idea, Chain, IdeaAuthor, \
    ChainLink, Actor, ChainEditor
from domain.idea_exchange.types import ChainID, IdeaID, ChainLinkID
from tests.fakes.dll.uow import FakeUOW
from random import randrange
from exceptions.auth import PermissionDenied
from framework.test.utils import generate_random_string
from exceptions.idea_exchange import IdeaIsNotEdiatable, ChainLinkCantBeDeleted
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
        self.chain_link1.number_of_related_ideas = 0
        self.chain_link2.number_of_related_ideas = 0
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

    def test_delete_chainlink_with_related_ideas(self):
        with self.assertRaises(ChainLinkCantBeDeleted):
            self.chain.replace_chain_links(
                [self.chain_link1]
            )

    def test_no_changed_chain_links(self):
        self.chain.replace_chain_links(
            [self.chain_link1, self.chain_link2]
        )
        self.assertEqual(2, len(list(self.chain.chain_links)))
        self.assertEqual(0, len(self.chain.dropped_chain_links))
        self.assertIn(self.chain_link1, self.chain.chain_links)
        self.assertIn(self.chain_link2, self.chain.chain_links)
        for i in self.chain.chain_links:
            self.assertFalse(i._meta.is_deleted)
            self.assertFalse(i._meta.is_changed)

    def test_changed_chain_links(self):
        changed_chain_link1 = ChainLinkFactory.create_chain_link(
            chain_link_id=self.chain_link1.chain_link_id,
            actor=self.chain_link1.actor,
            name=generate_random_string(10),
        )
        changed_chain_link1.set_for_change()
        self.chain.replace_chain_links(
            [changed_chain_link1, self.chain_link2]
        )
        self.assertEqual(2, len(list(self.chain.chain_links)))
        self.assertEqual(0, len(self.chain.dropped_chain_links))
        self.assertIn(changed_chain_link1, self.chain.chain_links)
        self.assertIn(self.chain_link2, self.chain.chain_links)
        self.assertTrue(self.chain.chain_links[0]._meta.is_changed)
        self.assertFalse(self.chain.chain_links[1]._meta.is_changed)