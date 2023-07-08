from typing import Callable

class LazyWrapper:
    
    def __init__(self, callable: Callable, params: dict) -> None:
        self._repo_method = callable
        self._params = params
    
    def fetch(self):
        return self._repo_method(**self._params)


class LazyLoaderInEntity():
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
    
    def __get__(self, obj, type=None):
        if not hasattr(obj, self.private_name):
            raise Exception(
                f"Field '{self.public_name}' not exists in {obj}, also check '{self.private_name}' in object in runtime"
            )
        value = getattr(obj, self.private_name)
        if isinstance(value, LazyWrapper):
            return value.fetch()
        return value

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

