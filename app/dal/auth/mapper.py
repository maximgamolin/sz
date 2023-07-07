from typing import TYPE_CHECKING

from app.framework.mapper import ABSMapper
from app.domain.auth.core import User
from app.domain.auth.core import UserID

if TYPE_CHECKING:
    from accounts.models import CustomUser


class UserMapper(ABSMapper):

    @staticmethod
    def from_orm_to_domain(orm_model: 'CustomUser') -> User:
        return User(
            user_id=UserID(orm_model.id)
        )
