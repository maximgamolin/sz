from unittest import TestCase
from cases.idea_exchange.idea import IdeaCase
from domain.idea_exchange.main import Idea, Chain, IdeaAuthor, \
    ChainLink, Actor, ChainEditor
from domain.idea_exchange.types import ChainID, IdeaID, ChainLinkID
from tests.fakes.dll.uow import FakeUOW
from random import randrange
from exceptions.auth import PermissionDenied
from exceptions.idea_exchange import IdeaIsNotEdiatable


class FakeChainUOW(FakeUOW):
    pass


class TestChainCases(TestCase):

    def test_true(self):
        self.assertTrue(True)

