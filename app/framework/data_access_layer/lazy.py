from typing import Callable, TypeVar, Generic, Union, Generator

T = TypeVar('T')

class LazyWrapper(Generic[T]):
    
    def __init__(self, callable: Callable, params: dict) -> None:
        self._repo_method = callable
        self._params = params
    
    def fetch(self):
        return self._repo_method(**self._params)



class LazyLoaderInEntity(Generic[T]):
    
    def __set_name__(self, owner, name: str):
        self.public_name = name
        self.private_name = '_lazy_wrapper_' + name
        self.cached_name = '_lazy_wrapper_cache_' + name

    def _process_lasy_wrapper(self, obj, value: LazyWrapper[T]) -> T:
        if not hasattr(obj, self.cached_name):
            new_value = value.fetch()
            if not isinstance(new_value, Generator):
                # TODO разобраться с механизмом кеширования генераторов, кастомный генератор придумать?
                setattr(obj, self.cached_name, new_value)
        else:
            new_value = getattr(obj, self.cached_name)
        return new_value

    def __get__(self, obj, type=None) -> T:
        if not hasattr(obj, self.private_name):
            raise Exception(
                f"Field '{self.public_name}' not exists in {obj}, also check '{self.private_name}' in object in runtime"
            )
        value = getattr(obj, self.private_name)
        if isinstance(value, LazyWrapper):
            return self._process_lasy_wrapper(obj, value)
        return value

    def __set__(self, obj: Union[LazyWrapper[T]|T|None], value) -> None:
        setattr(obj, self.private_name, value)

