from dataclasses import dataclass

from framework.data_access_layer.query_object import ABSQueryObject


@dataclass
class IdeaQO(ABSQueryObject):
    pass


@dataclass
class ChainQO(ABSQueryObject):
    pass


@dataclass
class AuthorQO(ABSQueryObject):
    pass


@dataclass
class ChainEditorQO(ABSQueryObject):
    pass


@dataclass
class ManagerQO(ABSQueryObject):
    pass


@dataclass
class ManagerOO(ABSQueryObject):
    pass
