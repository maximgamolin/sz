from typing import Optional

from dal.idea_exchange.dto import IdeaDtoFromOrm, ChainDtoFromOrm, ActorDtoFromOrm
from dal.idea_exchange.oo import IdeaOO, ChainOO, ActorOO
from dal.idea_exchange.qo import IdeaQO, ChainQO, ActorQO
from domain.auth.core import UserID
from domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID
from framework.data_access_layer.query_object import Empty
from framework.data_access_layer.vendor.django.repository import DjangoRepository
from idea.models import Idea, Chain, Actor


class IdeaRepository(DjangoRepository):

    model = Idea

    def __qo_to_filter_params(self, filter_params: IdeaQO) -> dict:
        filter_params_for_orm = {}
        if filter_params.author_id is not Empty():
            filter_params_for_orm['author_id'] = int(filter_params.author_id)
        if filter_params.idea_id is not Empty():
            filter_params_for_orm['id'] = int(filter_params.idea_id)
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

    def __orm_to_dto(self, idea: Idea) -> IdeaDtoFromOrm:
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


class ChainRepository(DjangoRepository):

    model = Chain

    def __qo_to_filter_params(self, filter_params: ChainQO) -> dict:
        filter_params_for_orm = {}
        if filter_params.chain_id is not Empty():
            filter_params_for_orm['id'] = filter_params.chain_id
        if filter_params.author_id is not Empty():
            filter_params_for_orm['author_id'] = filter_params.author_id
        if filter_params.reject_chain_link_id is not Empty():
            filter_params_for_orm['author_id'] = filter_params.author_id
        if filter_params.accept_chain_link_id is not Empty():
            filter_params_for_orm['accept_chain_link_id'] = filter_params.accept_chain_link_id
        if filter_params.is_deleted is not Empty():
            filter_params_for_orm['is_deleted'] = filter_params.is_deleted

    def __oo_to_order_params(self, order_params: ChainOO) -> dict:
        order_params_for_orm = {}
        if order_params.created_at is not Empty():
            order_params_for_orm['created_at'] = order_params.created_at
        return order_params_for_orm

    def __orm_to_dto(self, chain: Chain) -> ChainDtoFromOrm:
        return ChainDtoFromOrm(
            chain_id=ChainID(chain.id),
            actor_id=ActorID(chain.actor_id),
            author_id=UserID(chain.author_id),
            reject_chain_link=ChainLinkID(chain.reject_chain_link_id),
            accept_chain_link=ChainLinkID(chain.accept_chain_link_id),
            is_deleted=chain.is_deleted,
            created_at=chain.created_at,
            updated_at=chain.updated_at
        )


class ActorRepository(DjangoRepository):

    model = Actor

    def __orm_to_dto(self, orm_model: Actor) -> ActorDtoFromOrm:
        return ActorDtoFromOrm(
            actor_id=orm_model.id,
            name=orm_model.name
        )

    def __qo_to_filter_params(self, filter_params: Optional[ActorQO]) -> dict:
        filter_params_for_orm = {}
        if filter_params.name is not Empty():
            filter_params_for_orm['name'] = filter_params.name
        if filter_params.actor_id is not Empty():
            filter_params_for_orm['id'] = filter_params.actor_id
        return filter_params_for_orm

    def __oo_to_order_params(self, order_params: Optional[ActorOO]) -> dict:
        order_params_for_orm = {}
        if order_params.created_at is not Empty():
            order_params_for_orm['created_at'] = order_params.created_at
        return order_params_for_orm
