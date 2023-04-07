import abc
from typing import Generic, Iterable, Optional, TypeVar, Union

from app.exceptions.orm import NotFoundException
from app.framework.data_access_layer.basic import EntityTypeVar
from app.framework.data_access_layer.order_object.base import ABSOrderObject
from app.framework.data_access_layer.query_object.base import ABSQueryObject
from app.framework.domain.abs import IDTO, IEntity
from app.framework.mapper import ABSMapper

ModelEntityMapperClass = TypeVar('ModelEntityMapperClass', bound=ABSMapper)
ORMModel = TypeVar('ORMModel')
ISessionTypeVar = TypeVar('ISessionTypeVar')


class NoQueryBuilderRepositoryMixin:

    @abc.abstractmethod
    def _orm_to_dto(self, orm_model: ORMModel) -> Union[IDTO, IEntity]:
        pass

    @abc.abstractmethod
    def _qo_to_filter_params(self, filter_params: Optional[ABSQueryObject]) -> dict:
        pass

    @abc.abstractmethod
    def _oo_to_order_params(self, order_params: Optional[ABSOrderObject]) -> list:
        pass


class ABSRepository(abc.ABC):

    __slots__ = ('session', )

    mapper: Generic[ModelEntityMapperClass]

    def __init__(self, session: Generic[ISessionTypeVar]):
        self.session = session

    @abc.abstractmethod
    def exists(self, filter_params: Optional[ABSQueryObject]) -> bool:
        pass

    @abc.abstractmethod
    def count(self, filter_params: Optional[ABSQueryObject] = None) -> int:
        pass

    @abc.abstractmethod
    def fetch_one(
            self,
            filter_params: Optional[ABSQueryObject] = None,
            order_params: Optional[ABSOrderObject] = None,
            raise_if_empty: bool = True
    ) -> Optional[EntityTypeVar] | NotFoundException:
        pass

    @abc.abstractmethod
    def fetch_many(
            self,
            filter_params: Optional[ABSQueryObject] = None,
            order_params: Optional[ABSOrderObject] = None,
            offset: int = 0,
            limit: Optional[int] = None,
            chunk_size: int = 1000) -> Iterable[EntityTypeVar]:
        pass

    @abc.abstractmethod
    def add(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass

    @abc.abstractmethod
    def update_one(self, domain_model: Generic[EntityTypeVar]) -> None:
        pass
