from accounts.models import CustomUser, SiteGroup
from app.dal.auth.dto import SiteGroupDalDto
from app.domain.auth.core import User
from app.domain.auth.core import UserID, GroupID
from app.framework.data_access_layer.vendor.django.repository import DjangoRepository, OoOrmMapperLine, QoOrmMapperLine


class UserRepository(DjangoRepository):

    model = CustomUser

    def _orm_to_dto(self, orm_model: CustomUser) -> User:
        return User(
            user_id=UserID(orm_model.id)
        )

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        return [
            QoOrmMapperLine(qo_field_name='user_id',
                            orm_field_name='id',
                            modifier=int)
        ]

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        return []


class SiteGroupRepository(DjangoRepository):

    model = SiteGroup

    def _orm_to_dto(self, orm_model: SiteGroup) -> SiteGroupDalDto:
        return SiteGroupDalDto(
            group_id=GroupID(orm_model.id),
            name=orm_model.name,
            users_ids_in_group=list(CustomUser.groups.through.objects.filter(sitegroup_id=orm_model.id).values_list('customuser_id', flat=True))
        )

    @property
    def _qo_orm_fields_mapping(self) -> list[QoOrmMapperLine]:
        return [
            QoOrmMapperLine(orm_field_name='id',
                            qo_field_name='group_id',
                            modifier=int)
        ]

    @property
    def _oo_orm_fields_mapping(self) -> list[OoOrmMapperLine]:
        return []
