from unittest import TestCase

from app.tests.fakes.dll.uow import FakeUOW


class FakeChainUOW(FakeUOW):
    pass


class TestChainCases(TestCase):

    def test_true(self):
        self.assertTrue(True)

