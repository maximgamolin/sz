from typing import Optional

from cases.idea_exchange.dto import ChainLinkUserInputDTO, ActorUserInputDTO, IdeaUserDTO
from dal.auth.qo import UserQO, GroupQO
from dal.idea_exchange.oo import IdeaOO
from dal.idea_exchange.qo import IdeaQO, ChainQO, AuthorQO, ChainEditorQO, ManagerQO, ActorQO
from dal.idea_exchange.repo import IdeaRepository, ChainRepository
from domain.auth.core import User, Group
from domain.idea_exchange.main import IdeaAuthor, Chain, Idea, \
    ChainEditor, ChainLink, Actor, Manager
from framework.data_logic_layer.uow import BaseUnitOfWork


class IdeaUOW(BaseUnitOfWork):

    def __init__(
            self,
            idea_repo_cls=IdeaRepository,
            chain_repo_cls=ChainRepository
    ):
        self.idea_repo = idea_repo_cls(None)
        self.chain_repo = chain_repo_cls(None)


    def add_idea_for_save(self, idea: Idea):
        pass

    def fetch_author(self, query_object: AuthorQO) -> IdeaAuthor:
        pass

    def fetch_chain(self, query_object: ChainQO) -> Chain:
        pass

    def fetch_idea(self, query_object: IdeaQO) -> Idea:
        pass

    def fetch_manager(self, query_object: ManagerQO) -> Manager:
        pass

    def fetch_ideas(self, query_object: IdeaQO, order_object: Optional[IdeaOO] = None) -> list[Idea]:
        ideas_dtos = self.idea_repo.fetch_many(filter_params=query_object, order_params=order_object)
        for idea_dto in ideas_dtos:
            chain_qo = ChainQO(chain_id=idea_dto.chain_id)
            chian_dto = self.chain_repo.fetch_one(filter_params=query_object)
            actor_qo = ActorQO(actor_id=chian_dto.actor_id)


    def convert_idea_to_output(self, idea: Idea) -> IdeaUserDTO:
        pass


class ChainUOW(BaseUnitOfWork):

    def fetch_chain_editor(self, query_object: ChainEditorQO) -> ChainEditor:
        pass

    def fetch_actor(self, query_object: AuthorQO) -> Actor:
        pass

    def fetch_user(self, query_object: UserQO) -> User:
        # TODO Вынести в класс-извлекатор auth
        pass

    def fetch_group(self, query_object: GroupQO) -> Group:
        # TODO Вынести в класс-извлекатор auth
        pass

    def convert_actor_dto_to_entity(
            self,
            actor_user_input: ActorUserInputDTO
    ) -> Actor:
        # -! DoesNotExists
        users = []
        for user_id in actor_user_input.users_ids:
            user_qo = UserQO()
            user = self.fetch_user(query_object=user_qo)
            users.append(user)

        groups = []
        for group_id in actor_user_input.groups_ids:
            group_qo = GroupQO()
            group = self.fetch_group(query_object=group_qo)
            groups.append(group)

        return Actor(
            name=actor_user_input.name,
            users=users,
            groups=groups
        )

    def convert_chain_link_dto_to_entity(
            self,
            chain_link_user_input: ChainLinkUserInputDTO
    ) -> ChainLink:
        return ChainLink(
            chain_link_id=chain_link_user_input.chain_link_id,
            actor=self.convert_actor_dto_to_entity(chain_link_user_input.actor),
            name=chain_link_user_input.name,
            number_of_related_ideas=0,
            _meta_is_changed=bool(chain_link_user_input.chain_link_id is None)
        )

    def add_chain_for_save(self, chain: Chain):
        pass
