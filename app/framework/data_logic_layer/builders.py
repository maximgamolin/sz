from typing import TypeVar, Generic, Iterable

from app.framework.data_access_layer.lazy import LazyWrapper

T = TypeVar('T')

class BaseEntityFromRepoBuilder(Generic[T]):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
    def build_lazy_one(self) -> LazyWrapper[T]:
        raise NotImplementedError
    
    def build_lazy_many(self) -> LazyWrapper[Iterable[T]]:
        raise NotImplementedError
    
    def build_one(self) -> T:
        raise NotImplementedError
    
    def build_many(self) -> T:
        raise NotImplementedError
