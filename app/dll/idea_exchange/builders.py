from typing import Iterable, Type

from app.dal.auth.qo import SiteGroupQO
from app.dal.idea_exchange.dto import ActorDalDto
from app.dal.idea_exchange.dto import ChainLinkDalDto
from app.dal.idea_exchange.oo import ChainLinkOO
from app.dal.idea_exchange.qo import ManagerQO, ActorQO, ChainLinkQO
from app.domain.idea_exchange.main import Manager, ManagerGroup, Actor, ChainLink
from app.framework.data_access_layer.lazy import LazyWrapper
from app.framework.data_access_layer.query_object.values import IN
from app.framework.data_access_layer.repository import ABSRepository
from app.framework.data_logic_layer.builders import BaseEntityFromRepoBuilder


class ManagerBuilder(BaseEntityFromRepoBuilder):
    def __init__(self, manager_repo: ABSRepository, manager_qo: ManagerQO):
        super().__init__()
        self._manager_repo = manager_repo
        self._manager_qo = manager_qo
    
    def build_lazy_many(self) -> LazyWrapper:
        lazy = LazyWrapper(
            callable=self._manager_repo.fetch_many,
            params={"filter_params": self._manager_qo}
        )
        return lazy
    
    def build_many(self) -> Iterable[Manager]:
        return self._manager_repo.fetch_many(filter_params=self._manager_qo)


class ManagerGroupsBuilder(BaseEntityFromRepoBuilder):
    
    def __init__(
            self, 
            group_repo: ABSRepository, 
            group_qo: SiteGroupQO, 
            manager_builder: Type[BaseEntityFromRepoBuilder],
            manager_repo: ABSRepository
            ):
        super().__init__()
        self._group_repo = group_repo
        self._group_qo = group_qo
        self._manager_builder = manager_builder
        self._manager_repo = manager_repo
    
    def _build_lazy_many(self, *args, **kwargs) -> Iterable[ManagerGroup]:
        groups_dtos = self._group_repo.fetch_many(filter_params=self._group_qo)
        result = []
        for i in groups_dtos:
            manager_qo = ManagerQO(user_id=IN(i.users_ids_in_group))
            managers = self._manager_builder(
                manager_repo=self._manager_repo,
                manager_qo=manager_qo
            ).build_lazy_many()
            result.append(
                ManagerGroup(
                    group_id=i.group_id,
                    name=i.name,
                    managers=managers,
                )
            )
        return result
    
    def build_lazy_many(self):
        lazy = LazyWrapper(
            callable=self._build_lazy_many,
            params={}
        )
        return lazy


class ActorBuilder(BaseEntityFromRepoBuilder):
    
    def __init__(
            self, 
            actor_repo: ABSRepository,
            actor_qo: ActorQO,
            manager_groups_builder: Type['ManagerGroupsBuilder'],
            group_repo: ABSRepository, 
            manager_builder: Type[BaseEntityFromRepoBuilder],
            manager_repo: ABSRepository
        ):
        super().__init__()
        self._actor_repo = actor_repo
        self._actor_qo = actor_qo
        self._group_repo = group_repo
        self._manager_groups_builder = manager_groups_builder
        self._manager_builder = manager_builder
        self._manager_repo = manager_repo
    
    def _build_lazy_one(self, *args, **kwargs):
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
    
    def build_lazy(self):
        lazy = LazyWrapper(
            callable=self._build_lazy_one,
            params={}
        )
        return lazy

class ChainLinkBuilder(BaseEntityFromRepoBuilder):
    
    def __init__(
            self,
            chain_link_qo: ChainLinkQO,
            actor_builder: Type['ActorBuilder'],
            chain_link_oo: ChainLinkOO = None
        ):
        super().__init__()
        self._chain_link_qo = chain_link_qo
        self._chain_link_oo = chain_link_oo
        self._actor_builder = actor_builder
    
    def _build_chain_link(self, chain_link_dto: ChainLinkDalDto) -> ChainLink:
        actor_qo = ActorQO(actor_id=chain_link_dto.actor_id)
        actor = self._actor_builder(
            actor_repo=self.actor_repo,
            actor_qo=actor_qo,
            manager_groups_builder=ManagerGroupsBuilder,
            group_repo=self.group_repo,
            manager_builder=ManagerBuilder,
            manager_repo=self.manager_repository
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
        chain_link_dto: ChainLinkDalDto = self.chain_link_repository.fetch_one(filter_params=self.chain_link_qo)
        return self._build_chain_link(chain_link_dto)
    
    def build_lazy_one(self):
        lazy = LazyWrapper(
            callable=self._build_lazy_one,
            params={}
        )
        return lazy
    
    def _build_lazy_many(self) -> list[ChainLink]:
        params = {'filter_params': self._chain_link_qo}
        if self._chain_link_oo is not None:
            params['order_params'] = self._chain_link_oo
        chain_links_dtos: Iterable[ChainLinkDalDto] = self.chain_link_repository.fetch_many(**params)
        return [self._build_chain_link(i) for i in chain_links_dtos]
    
    def build_many(self):
        lazy = LazyWrapper(
            callable=self._build_lazy_many,
            params={}
        )
        return lazy