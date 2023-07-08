from typing import Optional, Iterable, Type

from app.cases.idea_exchange.dto import ChainLinkUiDto, ActorUiDto, IdeaUoDto, IdeaChanLinkUoDto
from app.dal.auth.qo import UserQO, SiteGroupQO
from app.dal.idea_exchange.dto import ActorDalDto, ChainLinkDalDto, IdeaDalDto, ChainDalDto
from app.dal.idea_exchange.oo import IdeaOO, ChainLinkOO
from app.dal.idea_exchange.qo import IdeaQO, ChainQO, AuthorQO, ChainEditorQO, ManagerQO, ActorQO, \
    ChainLinkQO
from app.domain.auth.core import User, Group
from app.domain.auth.core import UserID
from app.domain.idea_exchange.main import IdeaAuthor, Chain, Idea, \
    ChainEditor, ChainLink, Actor
from app.domain.idea_exchange.types import ChainLinkID, ChainID
from app.framework.data_access_layer.order_object.values import ASC
from app.framework.data_access_layer.query_object.values import IN
from app.framework.data_access_layer.repository import ABSRepository
from app.framework.data_logic_layer.uow import BaseUnitOfWork
from app.framework.injector.main import inject
from app.dll.idea_exchange.builders import ManagerBuilder, ManagerGroupsBuilder



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

    def add_idea_for_save(self, idea: Idea):
        pass

    def fetch_author(self, query_object: AuthorQO) -> IdeaAuthor:
        pass

    def fetch_idea(self, query_object: IdeaQO) -> Idea:
        pass
    
    def fetch_actor(self, actor_qo: ActorQO) -> Actor:
        actor_dto: ActorDalDto = self.actor_repo.fetch_one(filter_params=actor_qo)
        group_qo = SiteGroupQO(group_id=IN(actor_dto.groups_ids))
        manager_groups = ManagerGroupsBuilder(
            group_repo=self.group_repo,
            group_qo=group_qo,
            manager_builder=ManagerBuilder,
            manager_repo=self.manager_repository
        ).build_lazy()
        managers_qo = ManagerQO(user_id=IN(actor_dto.manager_ids))
        managers = ManagerBuilder(
            manager_repo=self.manager_repository,
            manager_qo=managers_qo
        ).build_lazy()
        return Actor(
            actor_id=actor_dto.actor_id,
            name=actor_dto.name,
            managers=managers,
            groups=manager_groups
        )

    def _build_chain_links(self, chain_link_dto: ChainLinkDalDto) -> ChainLink:
        actor_qo = ActorQO(actor_id=chain_link_dto.actor_id)
        actor = self.fetch_actor(actor_qo)
        return ChainLink(
                chain_link_id=chain_link_dto.chain_link_id,
                actor=actor,
                name=chain_link_dto.name,
                number_of_related_ideas=chain_link_dto.number_of_related_ideas,
                is_technical=chain_link_dto.is_technical,
                _meta_is_deleted=chain_link_dto.is_deleted
            )

    def fetch_chain_chain_links(self, chain_id: ChainID) -> list[ChainLink]:
        chain_link_qo = ChainLinkQO(
            is_technical=False,
            chain_id=chain_id,
            is_deleted=False
        )
        chain_link_oo = ChainLinkOO(
            order=ASC()
        )
        chain_links_dtos: Iterable[ChainLinkDalDto] = self.chain_link_repository.fetch_many(
            filter_params=chain_link_qo,
            order_params=chain_link_oo
        )
        result = []
        for chain_link_dto in chain_links_dtos:
            result.append(self._build_chain_links(chain_link_dto))
        return result

    def fetch_one_chain_link(self, chain_link_id: ChainLinkID):
        chain_link_qo = ChainLinkQO(
            chain_link_id=chain_link_id,
            is_deleted=False
        )
        chain_link_dto: ChainLinkDalDto = self.chain_link_repository.fetch_one(filter_params=chain_link_qo)
        return self._build_chain_links(chain_link_dto)

    def fetch_chain(self, chain_id: ChainID) -> Chain:
        chain_qo = ChainQO(chain_id=chain_id)
        chain_dto: ChainDalDto = self.chain_repo.fetch_one(filter_params=chain_qo)
        chain_links = self.fetch_chain_chain_links(chain_dto.chain_id)
        accept_chain_link = self.fetch_one_chain_link(chain_link_id=chain_dto.accept_chain_link_id)
        reject_chain_link = self.fetch_one_chain_link(chain_link_id=chain_dto.reject_chain_link_id)
        user_qo = UserQO(user_id=chain_dto.author_id)
        user_author = self.user_repo.fetch_one(filter_params=user_qo)
        return Chain(
            chain_id=chain_dto.chain_id,
            chain_links=chain_links,
            author=ChainEditor.from_user(user_author),
            reject_chain_link=reject_chain_link,
            accept_chain_link=accept_chain_link,
            _meta_is_deleted=chain_dto.is_deleted
        )

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

    def fetch_ideas(self, query_object: IdeaQO, order_object: Optional[IdeaOO] = None) -> list[Idea]:
        idea_dal_dtos: Iterable[IdeaDalDto] = self.idea_repo.fetch_many(filter_params=query_object, order_params=order_object)
        result = []
        for idea_dal_dto in idea_dal_dtos:
            result.append(
                self.build_idea(idea_dal_dto=idea_dal_dto)
            )
        return result

    def all_user_ideas(self, user_id: int):
        idea_qo = IdeaQO(
            author_id=UserID(user_id)
        )
        idea_oo = IdeaOO(
            created_at=ASC()
        )
        ideas = self.fetch_ideas(query_object=idea_qo, order_object=idea_oo)
        return [self.convert_idea_to_output(i).to_dict() for i in ideas]

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
