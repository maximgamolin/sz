from dataclasses import dataclass


class QueryParamComparison:
    pass


class Empty:

    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Empty, cls).__new__(cls)
        return cls._instance


class GTE(QueryParamComparison):

    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(GTE, cls).__new__(cls)
        return cls._instance


class ASC:

    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ASC, cls).__new__(cls)
        return cls._instance


class DESC:

    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DESC, cls).__new__(cls)
        return cls._instance


@dataclass
class ABSQueryObject:
    pass


@dataclass
class ABSOrderObject:
    pass
