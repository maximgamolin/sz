from typing import Iterable, Type

from app.framework.data_logic_layer.builders import BaseEntityFromRepoBuilder
from app.framework.data_access_layer.lazy import LazyWrapper
from app.framework.data_access_layer.repository import ABSRepository
from app.domain.idea_exchange.main import Manager, ManagerGroup
from app.dal.idea_exchange.qo import ManagerQO
from app.dal.auth.qo import SiteGroupQO
from app.framework.data_access_layer.query_object.values import IN


class ManagerBuilder(BaseEntityFromRepoBuilder):
    def __init__(self, manager_repo: ABSRepository, manager_qo: ManagerQO):
        self._manager_repo = manager_repo
        self._manager_qo = manager_qo
    
    def build_lazy(self) -> LazyWrapper:
        lazy = LazyWrapper(
            callable=self._manager_repo.fetch_many,
            params={"filter_params": self._manager_qo}
        )
        return lazy
    
    def build(self) -> Iterable[Manager]:
        return self._manager_repo.fetch_many(filter_params=self._manager_qo)


class ManagerGroupsBuilder(BaseEntityFromRepoBuilder):
    
    def __init__(
            self, 
            group_repo: ABSRepository, 
            group_qo: SiteGroupQO, 
            manager_builder: Type[BaseEntityFromRepoBuilder],
            manager_repo: 'ManagerBuilder'
            ):
        self._group_repo = group_repo
        self._group_qo = group_qo
        self._manager_builder = manager_builder
        self._manager_repo = manager_repo
    
    def _build_lazy(self, *args, **kwargs):
        groups_dtos = self._group_repo.fetch_many(filter_params=self._group_qo)
        result = []
        for i in groups_dtos:
            manager_qo = ManagerQO(user_id=IN(i.users_ids_in_group))
            managers = self._manager_builder(
                manager_repo=self._manager_repo,
                manager_qo=manager_qo
            ).build_lazy()
            result.append(
                ManagerGroup(
                    group_id=i.group_id,
                    name=i.name,
                    managers=managers,
                )
            )
        return result
    
    def build_lazy(self):
        lazy = LazyWrapper(
            callable=self._build_lazy,
            params={}
        )
        return lazy
    
    def build(self):
        raise NotImplementedError