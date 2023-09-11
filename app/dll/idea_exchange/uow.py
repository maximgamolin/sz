from typing import Optional, Iterable, Type

from app.cases.idea_exchange.dto import ChainLinkUiDto, ActorUiDto, IdeaUoDto, IdeaChanLinkUoDto
from app.dal.auth.qo import UserQO, SiteGroupQO
from app.dal.idea_exchange.dto import IdeaDalDto
from app.dal.idea_exchange.oo import IdeaOO
from app.dal.idea_exchange.qo import IdeaQO, ChainQO, AuthorQO, ChainEditorQO
from app.dll.idea_exchange.builders import ChainLinkBuilder, ChainBuilder
from app.domain.auth.core import User, Group
from app.domain.idea_exchange.main import IdeaAuthor, Chain, Idea, \
    ChainEditor, ChainLink, Actor
from app.domain.idea_exchange.types import ChainID
from app.framework.data_access_layer.repository import ABSRepository
from app.framework.data_logic_layer.uow import BaseUnitOfWork
from app.framework.injector.main import inject


class IdeaUOW(BaseUnitOfWork):

    def __init__(
            self,
            idea_repo_cls: Type[ABSRepository] = inject('IdeaRepository'),
            chain_repo_cls: Type[ABSRepository] = inject('ChainRepository'),
            actor_repo_cls: Type[ABSRepository] = inject('ActorRepository'),
            user_repo_cls: Type[ABSRepository] = inject('UserRepository'),
            group_repo_cls: Type[ABSRepository] = inject('SiteGroupRepository'),
            chain_link_repository_cls: Type[ABSRepository] = inject('ChainLinkRepository'),
            manager_repository: Type[ABSRepository] = inject('ManagerRepository')
    ):
        self.idea_repo = idea_repo_cls(None)
        self.chain_repo = chain_repo_cls(None)
        self.actor_repo = actor_repo_cls(None)
        self.user_repo = user_repo_cls(None)
        self.group_repo = group_repo_cls(None)
        self.chain_link_repository = chain_link_repository_cls(None)
        self.manager_repository = manager_repository(None)

    def fetch_chain(self, chain_id: ChainID) -> Chain:
        chain_qo = ChainQO(chain_id=chain_id)
        chain_builder = ChainBuilder(
            chain_repo=self.chain_repo,
            chain_qo=chain_qo,
            chain_link_builder_class=ChainLinkBuilder,
            chain_link_repo=self.chain_link_repository,
            actor_repo=self.actor_repo,
            group_repo=self.group_repo,
            manager_repo=self.manager_repository,
            user_repo=self.user_repo
        )
        return chain_builder.build_one()

    def build_idea(self, idea_dal_dto: IdeaDalDto) -> Idea:
        chain = self.fetch_chain(idea_dal_dto.chain_id)
        user_qo = UserQO(user_id=idea_dal_dto.author_id)
        user_author = self.user_repo.fetch_one(filter_params=user_qo)
        current_chain_link = chain.chain_link_by_id(idea_dal_dto.current_chain_link_id)
        return Idea(
            idea_id=idea_dal_dto.idea_id,
            author=IdeaAuthor.from_user(user_author),
            name=idea_dal_dto.name,
            body=idea_dal_dto.body,
            chain=chain,
            current_chain_link=current_chain_link,
            _meta_is_deleted=idea_dal_dto.is_deleted
        )

    def fetch_ideas(
            self,
            query_object: IdeaQO,
            order_object: Optional[IdeaOO] = None,
            offset: int = 0,
            limit: Optional[int] = None
    ) -> list[Idea]:
        idea_dal_dtos: Iterable[IdeaDalDto] = self.idea_repo.fetch_many(
            filter_params=query_object,
            order_params=order_object,
            offset=offset,
            limit=limit
        )
        result = []
        for idea_dal_dto in idea_dal_dtos:
            result.append(
                self.build_idea(idea_dal_dto=idea_dal_dto)
            )
        return result

    def convert_chain_link_to_uo(self, chain_link: ChainLink, idea: Idea) -> IdeaChanLinkUoDto:
        return IdeaChanLinkUoDto(
            chain_link_id=int(chain_link.chain_link_id),
            name=chain_link.name,
            is_current=idea.is_chain_link_current(chain_link)
        )

    def convert_idea_to_output(self, idea: Idea) -> IdeaUoDto:
        return IdeaUoDto(
            idea_id=idea.idea_id,
            name=idea.name,
            body=idea.body,
            is_accepted=idea.is_accepted(),
            is_rejected=idea.is_rejected(),
            chain_links=[self.convert_chain_link_to_uo(i, idea) for i in idea.chain.chain_links]
        )


class ChainUOW(BaseUnitOfWork):

    def fetch_chain_editor(self, query_object: ChainEditorQO) -> ChainEditor:
        pass

    def fetch_actor(self, query_object: AuthorQO) -> Actor:
        pass

    def fetch_user(self, query_object: UserQO) -> User:
        # TODO Вынести в класс-извлекатор auth
        pass

    def fetch_group(self, query_object: SiteGroupQO) -> Group:
        # TODO Вынести в класс-извлекатор auth
        pass

    def convert_actor_dto_to_entity(
            self,
            actor_user_input: ActorUiDto
    ) -> Actor:
        # -! DoesNotExists
        users = []
        for user_id in actor_user_input.users_ids:
            user_qo = UserQO()
            user = self.fetch_user(query_object=user_qo)
            users.append(user)

        groups = []
        for group_id in actor_user_input.groups_ids:
            group_qo = SiteGroupQO()
            group = self.fetch_group(query_object=group_qo)
            groups.append(group)

        return Actor(
            name=actor_user_input.name,
            managers=users,
            groups=groups
        )

    def convert_chain_link_dto_to_entity(
            self,
            chain_link_user_input: ChainLinkUiDto
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
