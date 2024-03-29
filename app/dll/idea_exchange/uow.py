from typing import Optional, Iterable, Type

from app.cases.idea_exchange.dto import ChainLinkUiDto, ActorUiDto, IdeaUoDto, IdeaChanLinkUoDto
from app.dal.auth.qo import UserQO, SiteGroupQO
from app.dal.idea_exchange.dto import IdeaDalDto
from app.dal.idea_exchange.oo import IdeaOO
from app.dal.idea_exchange.qo import IdeaQO, ChainQO, AuthorQO, ChainEditorQO
from app.dll.idea_exchange.builders import ChainLinkBuilder, ChainBuilder
from app.domain.auth.core import User, Group
from app.domain.auth.core import UserID
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
        self._idea_repo = idea_repo_cls(None)
        self._chain_repo = chain_repo_cls(None)
        self._actor_repo = actor_repo_cls(None)
        self._user_repo = user_repo_cls(None)
        self._group_repo = group_repo_cls(None)
        self._chain_link_repository = chain_link_repository_cls(None)
        self._manager_repository = manager_repository(None)
        self._domain_object_for_save = []

    def commit(self):
        ideas_for_save = [i for i in self._domain_object_for_save if isinstance(i, Idea)]
        self._idea_repo.add_many(ideas_for_save)
        self._domain_object_for_save = []


    def add_idea_for_save(self, idea: Idea) -> None:
        idea.set_updated_at_as_now()
        idea.mark_changed()
        self._domain_object_for_save.append(idea)


    def fetch_author(self, author_id: UserID) -> IdeaAuthor:
        user_qo = UserQO(user_id=author_id)
        user = self._user_repo.fetch_one(filter_params=user_qo)
        return IdeaAuthor.from_user(user)

    def fetch_chain(self, chain_id: ChainID) -> Chain:
        chain_qo = ChainQO(chain_id=chain_id)
        chain_builder = ChainBuilder(
            chain_repo=self._chain_repo,
            chain_qo=chain_qo,
            chain_link_builder_class=ChainLinkBuilder,
            chain_link_repo=self._chain_link_repository,
            actor_repo=self._actor_repo,
            group_repo=self._group_repo,
            manager_repo=self._manager_repository,
            user_repo=self._user_repo
        )
        return chain_builder.build_one()

    def build_idea(self, idea_dal_dto: IdeaDalDto) -> Idea:
        chain = self.fetch_chain(idea_dal_dto.chain_id)
        user_qo = UserQO(user_id=idea_dal_dto.author_id)
        user_author = self._user_repo.fetch_one(filter_params=user_qo)
        current_chain_link = chain.chain_link_by_id(idea_dal_dto.current_chain_link_id)
        return Idea(
            idea_storage_id=idea_dal_dto.idea_id,
            author=IdeaAuthor.from_user(user_author),
            name=idea_dal_dto.name,
            body=idea_dal_dto.body,
            chain=chain,
            idea_uid=idea_dal_dto.idea_uid,
            current_chain_link=current_chain_link,
            _meta_is_deleted=idea_dal_dto.is_deleted,
        )

    def fetch_idea(self, query_object: IdeaQO) -> Idea:
        idea_dal_dto: IdeaDalDto = self._idea_repo.fetch_one(filter_params=query_object)
        return self.build_idea(idea_dal_dto=idea_dal_dto)

    def fetch_ideas(
            self,
            query_object: IdeaQO,
            order_object: Optional[IdeaOO] = None,
            offset: int = 0,
            limit: Optional[int] = None
    ) -> list[Idea]:
        idea_dal_dtos: Iterable[IdeaDalDto] = self._idea_repo.fetch_many(
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
            chain_links=[self.convert_chain_link_to_uo(i, idea) for i in idea.chain.chain_links],
            idea_uid=idea.idea_uid
        )


class ChainUOW(BaseUnitOfWork):

    def __init__(
            self,
            chain_repo_cls: Type[ABSRepository] = inject('ChainRepository'),
            actor_repo_cls: Type[ABSRepository] = inject('ActorRepository'),
            user_repo_cls: Type[ABSRepository] = inject('UserRepository'),
            group_repo_cls: Type[ABSRepository] = inject('SiteGroupRepository'),
            chain_link_repository_cls: Type[ABSRepository] = inject('ChainLinkRepository'),
            manager_repository: Type[ABSRepository] = inject('ManagerRepository')
    ):
        self._chain_repo = chain_repo_cls(None)
        self._actor_repo = actor_repo_cls(None)
        self._user_repo = user_repo_cls(None)
        self._group_repo = group_repo_cls(None)
        self._chain_link_repository = chain_link_repository_cls(None)
        self._manager_repository = manager_repository(None)

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

    def fetch_chains(self, query_object: ChainQO) -> list[Chain]:
        chain_builder = ChainBuilder(
            chain_repo=self._chain_repo,
            chain_qo=query_object,
            chain_link_builder_class=ChainLinkBuilder,
            chain_link_repo=self._chain_link_repository,
            actor_repo=self._actor_repo,
            group_repo=self._group_repo,
            manager_repo=self._manager_repository,
            user_repo=self._user_repo
        )
        return list(chain_builder.build_many())

