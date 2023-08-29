from typing import Iterable, Type

from app.dal.auth.qo import SiteGroupQO
from app.dal.idea_exchange.dto import ActorDalDto
from app.dal.idea_exchange.dto import ChainLinkDalDto
from app.dal.idea_exchange.oo import ChainLinkOO
from app.dal.idea_exchange.qo import ManagerQO, ActorQO, ChainLinkQO
from app.domain.idea_exchange.main import Manager, ManagerGroup, Actor, ChainLink
from app.framework.data_access_layer.db_result_generator import DBResultGenerator
from app.framework.data_access_layer.lazy import LazyWrapper
from app.framework.data_access_layer.query_object.values import IN
from app.framework.data_access_layer.repository import ABSRepository
from app.framework.data_logic_layer.builders import ABSEntityFromRepoBuilder


class ManagerBuilder(ABSEntityFromRepoBuilder):
    def __init__(self, manager_repo: ABSRepository, manager_qo: ManagerQO):
        super().__init__()
        self._manager_repo = manager_repo
        self._manager_qo = manager_qo
    
    def build_lazy_many(self) -> LazyWrapper[DBResultGenerator[Manager]]:
        lazy = LazyWrapper(
            method=self._manager_repo.fetch_many,
            params={"filter_params": self._manager_qo}
        )
        return lazy
    
    def build_many(self) -> Iterable[Manager]:
        yield from self._manager_repo.fetch_many(filter_params=self._manager_qo)


class ManagerGroupsBuilder(ABSEntityFromRepoBuilder):
    
    def __init__(
            self, 
            group_repo: ABSRepository, 
            group_qo: SiteGroupQO, 
            manager_builder: Type[ABSEntityFromRepoBuilder],
            manager_repo: ABSRepository
            ):
        super().__init__()
        self._group_repo = group_repo
        self._group_qo = group_qo
        self._manager_builder = manager_builder
        self._manager_repo = manager_repo

    def _build_manager_group(self, group_dto):
        manager_qo = ManagerQO(user_id=IN(group_dto.users_ids_in_group))
        managers = self._manager_builder(
            manager_repo=self._manager_repo,
            manager_qo=manager_qo
        ).build_lazy_many()
        return ManagerGroup(
                group_id=group_dto.group_id,
                name=group_dto.name,
                managers=managers,
            )

    def _build_lazy_many(self, *args, **kwargs) -> DBResultGenerator[ManagerGroup]:
        groups_dtos = self._group_repo.fetch_many(filter_params=self._group_qo)
        return DBResultGenerator((self._build_manager_group(i) for i in groups_dtos))

    
    def build_lazy_many(self) -> LazyWrapper[Iterable[ManagerGroup]]:
        lazy = LazyWrapper(
            method=self._build_lazy_many,
            params={}
        )
        return lazy


class ActorBuilder(ABSEntityFromRepoBuilder):
    
    def __init__(
            self, 
            actor_repo: ABSRepository,
            actor_qo: ActorQO,
            manager_groups_builder: Type['ManagerGroupsBuilder'],
            group_repo: ABSRepository, 
            manager_builder: Type[ABSEntityFromRepoBuilder],
            manager_repo: ABSRepository
        ):
        super().__init__()
        self._actor_repo = actor_repo
        self._actor_qo = actor_qo
        self._group_repo = group_repo
        self._manager_groups_builder = manager_groups_builder
        self._manager_builder = manager_builder
        self._manager_repo = manager_repo
    
    def _build_lazy_one(self, *args, **kwargs) -> Actor:
        actor_dto: ActorDalDto = self._actor_repo.fetch_one(filter_params=self._actor_qo)
        group_qo = SiteGroupQO(group_id=IN(actor_dto.groups_ids))
        manager_groups = self._manager_groups_builder(
            group_repo=self._group_repo,
            group_qo=group_qo,
            manager_builder=self._manager_builder,
            manager_repo=self._manager_repo
        ).build_lazy_many()
        managers_qo = ManagerQO(user_id=IN(actor_dto.manager_ids))
        managers = self._manager_builder(
            manager_repo=self._manager_repo,
            manager_qo=managers_qo
        ).build_lazy_many()
        return Actor(
            actor_id=actor_dto.actor_id,
            name=actor_dto.name,
            managers=managers,
            groups=manager_groups
        )
    
    def build_lazy(self) -> LazyWrapper[Actor]:
        lazy = LazyWrapper(
            method=self._build_lazy_one,
            params={}
        )
        return lazy

class ChainLinkBuilder(ABSEntityFromRepoBuilder):
    
    def __init__(
            self,
            actor_repo: ABSRepository,
            group_repo: ABSRepository,
            manager_repo: ABSRepository,
            chain_link_repo: ABSRepository,
            chain_link_qo: ChainLinkQO,
            actor_builder: Type['ActorBuilder'],
            chain_link_oo: ChainLinkOO = None
        ):
        super().__init__()
        self._chain_link_qo = chain_link_qo
        self._chain_link_oo = chain_link_oo
        self._actor_builder = actor_builder
        self._actor_repo = actor_repo
        self._group_repo = group_repo
        self._manager_repo = manager_repo
        self._chain_link_repo = chain_link_repo
    
    def _build_chain_link(self, chain_link_dto: ChainLinkDalDto) -> ChainLink:
        actor_qo = ActorQO(actor_id=chain_link_dto.actor_id)
        actor = self._actor_builder(
            actor_repo=self._actor_repo,
            actor_qo=actor_qo,
            manager_groups_builder=ManagerGroupsBuilder,
            group_repo=self._group_repo,
            manager_builder=ManagerBuilder,
            manager_repo=self._manager_repo
        ).build_lazy()
        return ChainLink(
                chain_link_id=chain_link_dto.chain_link_id,
                actor=actor,
                name=chain_link_dto.name,
                number_of_related_ideas=chain_link_dto.number_of_related_ideas,
                is_technical=chain_link_dto.is_technical,
                _meta_is_deleted=chain_link_dto.is_deleted
            )
    
    def _build_lazy_one(self) -> ChainLink:
        chain_link_dto: ChainLinkDalDto = self._chain_link_repo.fetch_one(filter_params=self._chain_link_qo)
        return self._build_chain_link(chain_link_dto)
    
    def build_lazy_one(self) -> LazyWrapper[ChainLink]:
        lazy = LazyWrapper(
            method=self._build_lazy_one,
            params={}
        )
        return lazy
    
    def _build_lazy_many(self) -> Iterable[ChainLink]:
        params = {'filter_params': self._chain_link_qo}
        if self._chain_link_oo is not None:
            params['order_params'] = self._chain_link_oo
        chain_links_dtos: Iterable[ChainLinkDalDto] = self._chain_link_repo.fetch_many(**params)
        return DBResultGenerator((self._build_chain_link(i) for i in chain_links_dtos))
    
    def build_lazy_many(self) -> LazyWrapper[Iterable[ChainLink]]:
        lazy = LazyWrapper(
            method=self._build_lazy_many,
            params={}
        )
        return lazy