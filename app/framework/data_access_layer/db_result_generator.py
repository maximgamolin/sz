from itertools import chain
from typing import Generator, Generic, TypeVar

T = TypeVar('T')


class DBResultGenerator(Generic[T]):

    def __init__(self, db_generator: Generator):
        self._db_generator = db_generator
        self._cache: list[T] = []
        self._position = 1
        self._is_finished = False

    def drop_position(self) -> None:
        self._position = 1
        if self._is_finished:
            self._db_generator = iter(self._cache)
        else:
            self._db_generator = chain(self._cache, self._db_generator)

    def _add_value_to_cache(self, value):
        if self._position > len(self._cache) and not self._is_finished:
            self._cache.append(value)
        self._position += 1

    def __iter__(self):
        return self

    def __next__(self) -> T:
        try:
            result = next(self._db_generator)
        except StopIteration as e:
            self._is_finished = True
            raise e
        self._add_value_to_cache(result)
        return result