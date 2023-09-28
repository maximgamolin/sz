from typing import Type, Optional

from app.cases.idea_exchange.dto import IdeaUoDto
from app.dal.idea_exchange.oo import IdeaOO
from app.dal.idea_exchange.qo import IdeaQO, AuthorQO, ManagerQO
from app.dll.idea_exchange.uow import IdeaUOW
from app.domain.auth.core import UserID
from app.domain.idea_exchange.main import Idea
from app.domain.idea_exchange.types import IdeaID, ChainID
from app.exceptions.auth import PermissionDenied
from app.exceptions.idea_exchange import IdeaIsNotEdiatable, HasNoPermissions
from app.framework.data_access_layer.order_object.values import ASC


class IdeaCase:

    def __init__(self, uow_cls: Type[IdeaUOW] = IdeaUOW):
        self.uow = uow_cls()

    def user_ideas(self, author_id, offset: int = 0, limit: Optional[int] = None) -> list[IdeaUoDto]:
        with self.uow:
            idea_qo = IdeaQO(
                author_id=UserID(author_id),
            )
            idea_oo = IdeaOO(
                created_at=ASC()
            )
            ideas = self.uow.fetch_ideas(idea_qo, idea_oo, offset=offset, limit=limit)
            return [self.uow.convert_idea_to_output(i) for i in ideas]

    def fetch_idea(self, idea_uid: str) -> IdeaUoDto:
        with self.uow:
            idea_qo = IdeaQO(
                idea_uid=idea_uid
            )
            idea = self.uow.fetch_idea(idea_qo)
            return self.uow.convert_idea_to_output(idea)


    def create_idea(self, user_id: int, body: str, chain_id: int, name: str) -> Idea:
        with self.uow:
            author = self.uow.fetch_author(author_id = UserID(user_id))
            chain = self.uow.fetch_chain(chain_id=ChainID(chain_id))
            idea = Idea.initialize_new_idea(
                    body=body,
                    author=author,
                    chain=chain,
                    name=name
                )
            idea.set_created_at_as_now()
            self.uow.add_idea_for_save(idea=idea)
            self.uow.commit()
            return idea

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

    def fetch_allowed_chain_ids(self) -> list[ChainID]:
        with self.uow:
