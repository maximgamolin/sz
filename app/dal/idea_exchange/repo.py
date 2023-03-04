from typing import Generic, Optional, Iterable

from dal.idea_exchange.dto import IdeaDtoFromOrm
from dal.idea_exchange.oo import IdeaOO
from dal.idea_exchange.qo import IdeaQO
from domain.auth.core import UserID
from domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID
from exceptions.orm import NotFoundException
from framework.data_access_layer.basic import EntityTypeVar
from framework.data_access_layer.query_object import Empty, ABSQueryObject, ABSOrderObject
from framework.data_access_layer.repository import ABSRepository
from idea.models import Idea


class IdeaRepository(ABSRepository):

    def __qo_to_filter_params(self, filter_params: IdeaQO) -> dict:
        filter_params_for_orm = {}
        if filter_params.author_id is not Empty():
            filter_params_for_orm['author_id'] = int(filter_params.author_id)
        if filter_params.idea_id is not Empty():
            filter_params_for_orm['idea_id'] = int(filter_params.idea_id)
        if filter_params.name is not Empty():
            filter_params_for_orm['name'] = filter_params.name
        if filter_params.chain_id is not Empty():
            filter_params_for_orm['chain_id'] = int(filter_params.chain_id)
        if filter_params.current_chain_link_id is not Empty():
            filter_params_for_orm['current_chain_link_id'] = int(filter_params.current_chain_link_id)
        if filter_params.current_chain_link_id is not Empty():
            filter_params_for_orm['current_chain_link_id'] = int(filter_params.current_chain_link_id)
        if filter_params.is_deleted is not Empty():
            filter_params_for_orm['is_deleted'] = filter_params.is_deleted
        return filter_params_for_orm

    def __oo_to_order_params(self, order_params: IdeaOO) -> dict:
        order_params_for_orm = {}
        if order_params.created_at is not Empty():
            order_params_for_orm['created_at'] = order_params.created_at
        return order_params_for_orm

    def __idea_orm_to_idea_dto(self, idea: Idea) -> IdeaDtoFromOrm:
        return IdeaDtoFromOrm(
            idea_id=IdeaID(idea.id),
            author_id=UserID(idea.author_id),
            name=idea.name,
            body=idea.body,
            chain_id=ChainID(idea.chain_id),
            current_chain_link_id=ChainLinkID(idea.current_chain_link),
            is_deleted=idea.is_deleted,
            created_at=idea.created_at,
            updated_at=idea.updated_at
        )

    def exists(self, filter_params: Optional[IdeaQO]) -> bool:
        pass

    def count(self, filter_params: Optional[IdeaQO] = None) -> int:
        pass

    def fetch_one(
            self,
            filter_params: Optional[IdeaQO] = None,
            order_params: Optional[IdeaOO] = None,
            raise_if_empty: bool = True) -> Optional[IdeaDtoFromOrm] | NotFoundException:
        pass

    def fetch_many(
            self,
            filter_params: Optional[IdeaQO] = None,
            order_params: Optional[IdeaOO] = None,
            offset: int = 0, limit: Optional[int] = None,
            chunk_size: int = 1000) -> Iterable[IdeaDtoFromOrm]:
        if filter_params:
            filter_params_for_orm = self.__qo_to_filter_params(filter_params)
        else:
            filter_params_for_orm = {}
        if order_params:
            order_params_for_orm = self.__oo_to_order_params(order_params)
        else:
            order_params_for_orm = {}

        yield next(
            Idea.objects.filter(**filter_params_for_orm)
            .order_by(**order_params_for_orm)
            .iterator(chunk_size=chunk_size)
        )


    def add(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass

    def update_one(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass


class ChainRepository(ABSRepository):
    def exists(self, filter_params: Optional[ABSQueryObject]) -> bool:
        pass

    def count(self, filter_params: Optional[ABSQueryObject] = None) -> int:
        pass

    def fetch_one(
            self,
            filter_params: Optional[ABSQueryObject] = None,
            order_params: Optional[ABSOrderObject] = None,
            raise_if_empty: bool = True) -> Optional[EntityTypeVar] | NotFoundException:
        pass

    def fetch_many(self, filter_params: Optional[ABSQueryObject] = None, order_params: Optional[ABSOrderObject] = None,
                   offset: int = 0, limit: Optional[int] = None, chunk_size: int = 1000) -> Iterable[EntityTypeVar]:
        pass

    def add(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass

    def update_one(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass