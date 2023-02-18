from unittest import TestCase
from cases.idea_exchange.idea import IdeaCase
from domain.idea_exchange.main import Idea, Chain, IdeaAuthor, \
    ChainLink, Actor, ChainEditor
from domain.idea_exchange.types import ChainID, IdeaID, ChainLinkID
from tests.fakes.dll.uow import FakeUOW
from tests.factories.idea_exchange import ActorFactory, ChainEditorFactory, \
    ChainLinkFactory, ChainFactory, IdeaAuthorFactory, IdeaFactory, ManagerFactory, ManagerGroupFactory
from framework.test.utils import generate_random_string
from random import randrange
from exceptions.auth import PermissionDenied
from exceptions.idea_exchange import IdeaIsNotEdiatable, HasNoPermissions


class FakeIdeaUOW(FakeUOW):

    def __init__(
            self,
            *args,
            chain=None,
            author=None,
            idea=None,
            manager=None,
            **kwargs
    ):
        self.idea = None
        self.__chain = chain
        self.__author = author
        self.__idea = idea
        self.__manager = manager

    def __call__(self, *args, **kwargs):
        return self

    def convert_user_to_author(self, *args, **kwargs):
        return None

    def fetch_chain(self, *args, **kwargs):
        return self.__chain

    def fetch_author(self, *args, **kwargs):
        return self.__author

    def fetch_idea(self, *args, **kwargs):
        return self.__idea

    def add_idea_for_save(self, idea):
        self.idea = idea

    def fetch_manager(self, *args, **kwargs):
        return self.__manager


class TestIdeaExchangeCases(TestCase):

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
        self.author = IdeaAuthorFactory.create_idea_author()
        self.idea = IdeaFactory.create_idea(
            author=self.author,
            chain=self.chain,
            current_chain_link=self.chain_link1,
            meta_is_changed=False,
            meta_is_deleted=False
        )

    def test_create_new_idea(self):
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author
        )
        case = IdeaCase(uow_cls=uow)
        case.create_idea(user_id=1, body=generate_random_string(10), chain_id=1)
        self.assertIsNotNone(uow.idea)
        self.assertIsInstance(uow.idea, Idea)
        self.assertEqual(uow.idea.author, self.author)
        self.assertEqual(uow.idea.chain, self.chain)
        self.assertTrue(uow.idea._meta.is_changed)

    def test_correct_delete_idea(self):
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            idea=self.idea
        )
        case = IdeaCase(uow_cls=uow)
        case.delete_idea(user_id=self.author.user_id, idea_id=self.idea.idea_id)
        self.assertTrue(uow.idea._meta.is_deleted)
        self.assertTrue(uow.idea._meta.is_changed)

    def test_incorrect_author_delete_idea(self):
        incorrect_author = IdeaAuthor(user_id=self.author.user_id+1)
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=incorrect_author,
            idea=self.idea
        )
        case = IdeaCase(uow_cls=uow)
        with self.assertRaises(PermissionDenied):
            case.delete_idea(user_id=incorrect_author.user_id, idea_id=self.idea.idea_id)

    def test_update_idea(self):
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            idea=self.idea
        )
        new_body = generate_random_string(10)
        case = IdeaCase(uow_cls=uow)
        case.edit_idea(
            user_id=self.author.user_id,
            body=new_body,
            idea_id=self.idea.idea_id
        )
        self.assertEqual(uow.idea.body, new_body)
        self.assertTrue(uow.idea._meta.is_changed)

    def test_update_idea_user_dont_have_permissions(self):
        incorrect_author = IdeaAuthor(user_id=self.author.user_id + 1)
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=incorrect_author,
            idea=self.idea
        )
        new_body = generate_random_string(10)
        case = IdeaCase(uow_cls=uow)
        with self.assertRaises(PermissionDenied):
            case.edit_idea(user_id=incorrect_author.user_id, idea_id=self.idea.idea_id, body=new_body)

    def test_update_idea_on_wrong_chain_link(self):
        idea = Idea(
            idea_id=IdeaID(randrange(1, 100)),
            author=self.author,
            body='123',
            chain=self.chain,
            current_chain_link=self.chain_link2,
            _meta_is_changed=False,
            _meta_is_deleted=False
        )
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            idea=idea
        )
        case = IdeaCase(uow_cls=uow)
        new_body = generate_random_string(10)
        with self.assertRaises(IdeaIsNotEdiatable):
            case.edit_idea(
                user_id=self.author.user_id,
                body=new_body,
                idea_id=self.idea.idea_id
            )

    def test_accept_idea_to_next_step(self):
        manager = ManagerFactory.create_manager()
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            manager=manager,
            idea=self.idea
        )

        actor = ActorFactory.create_actor(managers=[manager])
        self.chain_link1.actor = actor
        case = IdeaCase(uow_cls=uow)
        case.accept_idea(manager.user_id, self.idea.idea_id)
        self.assertEqual(self.idea.current_chain_link, self.chain_link2)
        self.assertTrue(self.idea._meta.is_changed)

    def test_accept_idea_to_last_step(self):
        manager = ManagerFactory.create_manager()
        self.idea.current_chain_link = self.chain_link2
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            manager=manager,
            idea=self.idea
        )
        actor = ActorFactory.create_actor(managers=[manager])
        self.chain_link2.actor = actor
        case = IdeaCase(uow_cls=uow)
        case.accept_idea(manager.user_id, self.idea.idea_id)
        self.assertEqual(self.idea.current_chain_link, self.chain.accept_chain_link)
        self.assertTrue(self.idea._meta.is_changed)

    def test_accept_idea_as_group_member(self):
        self.assertEqual(self.idea.current_chain_link, self.chain_link1)
        self.assertFalse(self.idea._meta.is_changed)
        manager = ManagerFactory.create_manager()
        manager_group = ManagerGroupFactory.create_manager_group(managers=[manager])
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            manager=manager,
            idea=self.idea
        )
        actor = ActorFactory.create_actor(groups=[manager_group])
        self.chain_link1.actor = actor
        case = IdeaCase(uow_cls=uow)
        case.accept_idea(manager.user_id, self.idea.idea_id)
        self.assertEqual(self.idea.current_chain_link, self.chain_link2)
        self.assertTrue(self.idea._meta.is_changed)

    def test_error_manager_is_not_actor(self):
        manager = ManagerFactory.create_manager()
        uow = FakeIdeaUOW(
            chain=self.chain,
            author=self.author,
            manager=manager,
            idea=self.idea
        )
        case = IdeaCase(uow_cls=uow)
        with self.assertRaises(HasNoPermissions):
            case.accept_idea(manager.user_id, self.idea.idea_id)
