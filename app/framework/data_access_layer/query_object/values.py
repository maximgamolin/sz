from abc import ABC
from typing import Any

class QueryParamComparison(ABC):
    """
    Базовый класс для управления параметрами фильтрации, используется только с ABSOrderObject
    """
    def __init__(self, value: Any):
        self.value = value


class GTE(QueryParamComparison):
    """
    Эквивалент <=
    """


class IN(QueryParamComparison):
    """
    Для проверки элементов в списке
    """
