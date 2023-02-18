from domain.idea_exchange.main import Idea
from domain.idea_exchange.types import IdeaID
from typing import Type
from dll.idea_exchange.uow import IdeaUOW
from dal.idea_exchange.qo import IdeaQO, ChainQO, AuthorQO, ManagerQO, ManagerOO
from exceptions.auth import PermissionDenied
from exceptions.idea_exchange import IdeaIsNotEdiatable, HasNoPermissions


class IdeaCase:

    def __init__(self, uow_cls: Type[IdeaUOW]):
        self.uow = uow_cls()

    def create_idea(self, user_id: int, body: str, chain_id: int) -> None:
        with self.uow:
            chain_qo = ChainQO()
            author_qo = AuthorQO()
            author = self.uow.fetch_author(author_qo)
            chain = self.uow.fetch_chain(chain_qo)
            idea = Idea.initialize_new_idea(
                    body=body,
                    author=author,
                    chain=chain
                )
            self.uow.add_idea_for_save(idea=idea)
            self.uow.commit()

    def delete_idea(self, user_id: int, idea_id: IdeaID):
        with self.uow:
            author_qo = AuthorQO()
            author = self.uow.fetch_author(author_qo)
            idea_qo = IdeaQO()
            idea = self.uow.fetch_idea(idea_qo)
            if not author.can_delete_idea(idea):
                raise PermissionDenied()
            idea.mark_deleted()
            self.uow.add_idea_for_save(idea)
            self.uow.commit()

    def edit_idea(self, user_id: int, body: str, idea_id: int):
        with self.uow:
            author_qo = AuthorQO()
            author = self.uow.fetch_author(author_qo)
            idea_qo = IdeaQO()
            idea = self.uow.fetch_idea(idea_qo)
            if not author.can_edit_idea(idea):
                raise PermissionDenied()
            if not idea.is_editable():
                raise IdeaIsNotEdiatable()
            idea.update(
                body=body
            )
            self.uow.add_idea_for_save(idea)
            self.uow.commit()

    def accept_idea(self, user_id: int, idea_id: int):
        with self.uow:
            manager_qo = ManagerQO()
            manager = self.uow.fetch_manager(manager_qo)
            idea_qo = IdeaQO()
            idea = self.uow.fetch_idea(idea_qo)
            if not idea.is_manager_valid_actor(manager):
                raise HasNoPermissions('User cant manage this idea')
            idea.move_to_next_chain_link()
            self.uow.add_idea_for_save(idea)
            self.uow.commit()

    def reject_idea(self):
        with self.uow:
            manager_qo = ManagerQO()
            manager = self.uow.fetch_manager(manager_qo)
            idea_qo = IdeaQO()
            idea = self.uow.fetch_idea(idea_qo)
            if not idea.is_manager_valid_actor(manager):
                raise HasNoPermissions('User cant manage this idea')
            idea.reject_idea()
            self.uow.add_idea_for_save(idea)
            self.uow.commit()
