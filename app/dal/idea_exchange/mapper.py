from typing import TYPE_CHECKING

from app.framework.mapper import ABSMapper

from app.domain.idea_exchange.main import Manager
from app.domain.auth.core import UserID


if TYPE_CHECKING:
    from accounts.models import CustomUser

class ManagerMapper(ABSMapper):

    @staticmethod
    def from_orm_to_domain(orm_model: 'CustomUser') -> Manager:
        return Manager(
            user_id=UserID(orm_model.id)
        )
