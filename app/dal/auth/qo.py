from dataclasses import dataclass
from typing import Optional, Union

from app.domain.auth.core import UserID, GroupID
from app.framework.data_access_layer.query_object.base import ABSQueryObject
from app.framework.data_access_layer.query_object.values import QueryParamComparison
from app.framework.data_access_layer.values import Empty


@dataclass
class UserQO(ABSQueryObject):
    user_id: Optional[Union[UserID, QueryParamComparison, Empty]] = Empty()


@dataclass
class SiteGroupQO(ABSQueryObject):
    group_id: Optional[Union[GroupID, QueryParamComparison, Empty]] = Empty()

