from abc import ABC
from typing import Generic, Optional, Iterable

from exceptions.orm import NotFoundException
from framework.data_access_layer.basic import EntityTypeVar
from framework.data_access_layer.query_object import ABSQueryObject, ABSOrderObject
from framework.data_access_layer.repository import ABSRepository, ORMModel, NoQueryBuilderRepositoryMixin


class DjangoRepository(ABSRepository, NoQueryBuilderRepositoryMixin, ABC):

    model: ORMModel = None

    def exists(self, filter_params: Optional[ABSQueryObject]) -> bool:
        pass

    def count(self, filter_params: Optional[ABSQueryObject] = None) -> int:
        pass

    def fetch_one(
            self,
            filter_params: Optional[ABSQueryObject] = None,
            order_params: Optional[ABSOrderObject] = None,
            raise_if_empty: bool = True
    ) -> Optional[EntityTypeVar] | NotFoundException:
        if filter_params:
            filter_params_for_orm = self.__qo_to_filter_params(filter_params)
        else:
            filter_params_for_orm = {}
        if order_params:
            order_params_for_orm = self.__oo_to_order_params(order_params)
        else:
            order_params_for_orm = {}
        orm_chan = self.model.objects.filter(
            **filter_params_for_orm
        ).order_by(
            **order_params_for_orm
        ).first()
        if not orm_chan:
            return
        return self.__orm_to_dto(orm_chan)

    def fetch_many(
            self,
            filter_params: Optional[ABSQueryObject] = None,
            order_params: Optional[ABSOrderObject] = None,
            offset: int = 0,
            limit: Optional[int] = None,
            chunk_size: int = 1000
    ) -> Iterable[EntityTypeVar]:
        if filter_params:
            filter_params_for_orm = self.__qo_to_filter_params(filter_params)
        else:
            filter_params_for_orm = {}
        if order_params:
            order_params_for_orm = self.__oo_to_order_params(order_params)
        else:
            order_params_for_orm = {}
        orm_ideas = self.model.objects.filter(
            **filter_params_for_orm
        ).order_by(
            **order_params_for_orm
        ).iterator(chunk_size=chunk_size)
        for orm_idea in orm_ideas:
            yield self.__orm_to_dto(orm_idea)

    def add(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass

    def update_one(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass