from typing import Optional

from accounts.models import CustomUser, SiteGroup
from dal.auth.dto import SiteGroupDalDto
from dal.auth.oo import UserOO, SiteGroupOO
from dal.auth.qo import UserQO, SiteGroupQO
from domain.auth.core import User
from domain.auth.core import UserID, GroupID
from framework.data_access_layer.query_object.values import IN
from framework.data_access_layer.values import Empty
from framework.data_access_layer.vendor.django.repository import DjangoRepository


class UserRepository(DjangoRepository):

    def __orm_to_dto(self, orm_model: CustomUser) -> User:
        return User(
            user_id=UserID(orm_model.id)
        )

    def __qo_to_filter_params(self, filter_params: Optional[UserQO]) -> dict:
        filter_params_for_orm = {}
        if filter_params.user_id is not Empty():
            if isinstance(filter_params.user_id, IN):
                filter_params_for_orm['id__in'] = filter_params.user_id.value
            else:
                filter_params_for_orm['id'] = int(filter_params.user_id)
        return filter_params_for_orm

    def __oo_to_order_params(self, order_params: Optional[UserOO]) -> list:
        return []


class SiteGroupRepository(DjangoRepository):

    def __orm_to_dto(self, orm_model: SiteGroup) -> SiteGroupDalDto:
        return SiteGroupDalDto(
            group_id=GroupID(orm_model.id),
            name=orm_model.name,
            users_ids_in_group=orm_model.user_set.values_list('id', flat=True)
        )

    def __qo_to_filter_params(self, filter_params: Optional[SiteGroupQO]) -> dict:
        filter_params_for_orm = {}
        if filter_params.group_id is not Empty():
            if isinstance(filter_params.group_id, IN):
                filter_params_for_orm['id__in'] = filter_params.group_id.value
            else:
                filter_params_for_orm['id'] = int(filter_params.group_id)
        return filter_params_for_orm

    def __oo_to_order_params(self, order_params: Optional[SiteGroupOO]) -> list:
        return []
