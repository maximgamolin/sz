from typing import TYPE_CHECKING

from app.dal.auth.repo import UserRepository
from app.dal.idea_exchange.dto import IdeaDalDto, ChainDalDto, ActorDalDto, ChainLinkDalDto
from app.dal.idea_exchange.mapper import ManagerMapper
from app.domain.auth.core import UserID
from app.domain.idea_exchange.types import IdeaID, ChainID, ChainLinkID, ActorID
from app.framework.data_access_layer.vendor.django.repository import DjangoRepository, OoOrmMapperLine, QoOrmMapperLine
from idea.models import Idea, Chain, Actor, ChainLink

if TYPE_CHECKING:
    from app.domain.idea_exchange.main import Idea as DomainIdea, Chain as DomainChain, \
        ChainLink as DomainChainLink, Actor as DomainActor
    from accounts.models import CustomUser
    from app.domain.idea_exchange.main import Manager as DomainManager


class IdeaRepository(DjangoRepository):

    model = Idea

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        return [
            QoOrmMapperLine(orm_field_name='id',
                            qo_field_name='idea_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='author_id',
                            qo_field_name='author_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='name',
                            qo_field_name='name'),
            QoOrmMapperLine(orm_field_name='chain_id',
                            qo_field_name='chain_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='current_chain_link_id',
                            qo_field_name='current_chain_link_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='is_deleted',
                            qo_field_name='is_deleted'),
            QoOrmMapperLine(orm_field_name='idea_uid',
                            qo_field_name='idea_uid'),
        ]

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        return [
            OoOrmMapperLine(orm_field_name='created_at',
                            oo_field_name='created_at')
        ]

    def _orm_to_dto(self, idea: Idea) -> IdeaDalDto:
        return IdeaDalDto(
            idea_id=IdeaID(idea.id),
            author_id=UserID(idea.author_id),
            name=idea.name,
            body=idea.body,
            chain_id=ChainID(idea.chain_id),
            current_chain_link_id=ChainLinkID(idea.current_chain_link_id),
            is_deleted=idea.is_deleted,
            created_at=idea.created_at,
            updated_at=idea.updated_at,
            idea_uid=idea.idea_uid
        )

    def _dto_to_orm(self, dto: 'DomainIdea') -> Idea:
        return Idea(
            id=dto.idea_id,
            author_id=dto.get_author_id(),
            name=dto.name,
            body=dto.body,
            idea_uid=dto.get_idea_uid(),
            chain_id=dto.get_chain_id(),
            current_chain_link_id=dto.get_current_chain_link_id(),
            is_deleted=dto.is_deleted(),
            created_at=dto.get_created_at(),
            updated_at=dto.get_updated_at(),
        )



class ChainRepository(DjangoRepository):

    model = Chain

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        return [
            QoOrmMapperLine(orm_field_name='id',
                            qo_field_name='chain_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='author_id',
                            qo_field_name='author_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='accept_chain_link_id',
                            qo_field_name='accept_chain_link_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='reject_chain_link_id',
                            qo_field_name='reject_chain_link_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='is_deleted',
                            qo_field_name='is_deleted'),
        ]

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        return [
            OoOrmMapperLine(orm_field_name='created_at',
                            oo_field_name='created_at')
        ]

    def _orm_to_dto(self, chain: Chain) -> ChainDalDto:
        return ChainDalDto(
            chain_id=ChainID(chain.id),
            author_id=UserID(chain.author_id),
            reject_chain_link_id=ChainLinkID(chain.reject_chain_link_id),
            accept_chain_link_id=ChainLinkID(chain.accept_chain_link_id),
            is_deleted=chain.is_deleted,
            created_at=chain.created_at,
            updated_at=chain.updated_at
        )

    def _dto_to_orm(self, dto: 'DomainChain') -> Chain:
        pass


class ChainLinkDjangoRepository(DjangoRepository):

    model = ChainLink

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        return [
            QoOrmMapperLine(orm_field_name='id',
                            qo_field_name='chain_link_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='chain_id',
                            qo_field_name='chain_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='is_technical',
                            qo_field_name='is_technical'),
            QoOrmMapperLine(orm_field_name='actor_id',
                            qo_field_name='actor_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='is_deleted',
                            qo_field_name='is_deleted'),
        ]

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        return [
            OoOrmMapperLine(orm_field_name='created_at',
                            oo_field_name='created_at'),
            OoOrmMapperLine(orm_field_name='order',
                            oo_field_name='order'),
        ]

    def _orm_to_dto(self, orm_model: ChainLink) -> ChainLinkDalDto:
        return ChainLinkDalDto(
            chain_link_id=ChainLinkID(orm_model.id),
            actor_id=ActorID(orm_model.actor_id),
            name=orm_model.name,
            is_technical=orm_model.is_technical,
            order=orm_model.order,
            chain_id=ChainID(orm_model.chain_id),
            number_of_related_ideas=orm_model.idea_set.count(),
            is_deleted=orm_model.is_deleted
        )

    def _dto_to_orm(self, dto: 'DomainChainLink') -> ChainLink:
        pass


class ActorRepository(DjangoRepository):

    model = Actor

    def _orm_to_dto(self, orm_model: Actor) -> ActorDalDto:
        return ActorDalDto(
            actor_id=ActorID(orm_model.id),
            name=orm_model.name,
            manager_ids=list(orm_model.managers.values_list('id', flat=True)),
            groups_ids=list(orm_model.groups.values_list('id', flat=True))
        )

    def _dto_to_orm(self, dto: 'DomainActor') -> Actor:
        pass

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        return [
            QoOrmMapperLine(orm_field_name='id',
                            qo_field_name='actor_id',
                            modifier=int),
            QoOrmMapperLine(orm_field_name='name',
                            qo_field_name='name'),
        ]

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        return [
            OoOrmMapperLine(orm_field_name='created_at',
                            oo_field_name='created_at')
        ]


class ManagerRepository(UserRepository):

    def _orm_to_dto(self, orm_model: 'CustomUser') -> 'DomainManager':
        return ManagerMapper().from_orm_to_domain(orm_model)