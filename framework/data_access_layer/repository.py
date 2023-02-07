import abc
from typing import Generic, Iterable, Optional, TypeVar

from framework.data_access_layer.basic import EntityTypeVar
from framework.mapper import ABSMapper
from framework.data_access_layer.query_object import ABSQueryObject, ABSOrderObject
from exceptions.orm import NotFoundException

ModelEntityMapperClass = TypeVar('ModelEntityMapperClass', bound=ABSMapper)
ISessionTypeVar = TypeVar('ISessionTypeVar')


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
