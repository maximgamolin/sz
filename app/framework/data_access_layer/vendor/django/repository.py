from abc import ABC
from typing import Generic, Optional, Callable, Any

from app.exceptions.orm import NotFoundException
from app.framework.data_access_layer.basic import EntityTypeVar
from app.framework.data_access_layer.db_result_generator import DBResultGenerator
from app.framework.data_access_layer.order_object.base import ABSOrderObject
from app.framework.data_access_layer.order_object.values import ASC, DESC
from app.framework.data_access_layer.query_object.base import ABSQueryObject
from app.framework.data_access_layer.query_object.values import IN, GTE
from app.framework.data_access_layer.repository import ABSRepository, ORMModel, NoQueryBuilderRepositoryMixin
from app.framework.data_access_layer.values import Empty


class QoOrmMapperLine:

    __slots__ = 'orm_field_name', 'qo_field_name', 'modifier'

    def __init__(self, orm_field_name: str, qo_field_name: str, modifier: Optional[Callable[[Any], Any]] = None):
        self.orm_field_name = orm_field_name
        self.qo_field_name = qo_field_name
        self.modifier = modifier or (lambda x: x)


class OoOrmMapperLine:

    __slots__ = 'orm_field_name', 'oo_field_name'

    def __init__(self, orm_field_name: str, oo_field_name: str):
        self.orm_field_name = orm_field_name
        self.oo_field_name = oo_field_name


class DjangoNoQueryBuilderRepositoryMixin(NoQueryBuilderRepositoryMixin, ABC):

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        raise NotImplementedError()

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        raise NotImplementedError()

    def _extract_filter_val_for_orm(self, mapper_line: QoOrmMapperLine, val) -> dict:
        if isinstance(val, IN):
            orm_query_param_name = f'{mapper_line.orm_field_name}__in'
            value = [mapper_line.modifier(i) for i in val.value]
        elif isinstance(val, GTE):
            orm_query_param_name = f'{mapper_line.orm_field_name}__gte'
            value = mapper_line.modifier(val.value)
        else:
            orm_query_param_name = mapper_line.orm_field_name
            value = mapper_line.modifier(val)
        return {orm_query_param_name: value}


    def _qo_to_filter_params(self, filter_params: Optional[ABSQueryObject]) -> dict:
        if not filter_params:
            return {}
        filter_params_for_orm = {}
        for mapper_line in self._qo_orm_fields_mapping:
            field_val = getattr(filter_params, mapper_line.qo_field_name)
            if field_val is Empty():
                continue
            filter_params_for_orm.update(
                self._extract_filter_val_for_orm(mapper_line, field_val)
            )
        return filter_params_for_orm

    def _extract_order_values_to_orm(self, mapper_line: OoOrmMapperLine, val) -> str:
        if isinstance(val, ASC):
            return mapper_line.orm_field_name
        if isinstance(val, DESC):
            return f'-{mapper_line.orm_field_name}'

    def _oo_to_order_params(self, order_params: Optional[ABSOrderObject]) -> list:
        if not order_params:
            return []
        order_params_for_orm = []
        for mapper_line in self._oo_orm_fields_mapping:
            field_val = getattr(order_params, mapper_line.oo_field_name)
            if field_val is Empty():
                continue
            order_params_for_orm.append(self._extract_order_values_to_orm(mapper_line, field_val))
        return order_params_for_orm


class DjangoRepository(ABSRepository, DjangoNoQueryBuilderRepositoryMixin, ABC):

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
            filter_params_for_orm = self._qo_to_filter_params(filter_params)
        else:
            filter_params_for_orm = {}
        if order_params:
            order_params_for_orm = self._oo_to_order_params(order_params)
        else:
            order_params_for_orm = []
        orm_chan = self.model.objects.filter(
            **filter_params_for_orm
        ).order_by(
            *order_params_for_orm
        ).first()
        if not orm_chan:
            return
        return self._orm_to_dto(orm_chan)

    def fetch_many(
            self,
            filter_params: Optional[ABSQueryObject] = None,
            order_params: Optional[ABSOrderObject] = None,
            offset: int = 0,
            limit: Optional[int] = None,
            chunk_size: int = 1000
    ) -> DBResultGenerator[EntityTypeVar]:
        orm_ideas = self.model.objects
        if filter_params:
            filter_params_for_orm = self._qo_to_filter_params(filter_params)
            orm_ideas = orm_ideas.filter(**filter_params_for_orm)

        if order_params:
            order_params_for_orm = self._oo_to_order_params(order_params)
            orm_ideas = orm_ideas.order_by(*order_params_for_orm)

        orm_ideas.iterator(chunk_size=chunk_size)
        return DBResultGenerator((self._orm_to_dto(i) for i in orm_ideas))

    def add(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass

    def update_one(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass