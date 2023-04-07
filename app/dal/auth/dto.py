from dataclasses import dataclass

from app.domain.auth.core import UserID, GroupID


@dataclass
class SiteGroupDalDto:
    group_id: GroupID
    name: str
    users_ids_in_group: list[UserID]
