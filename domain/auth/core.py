from dataclasses import dataclass
from typing import NewType

UserID = NewType('UserID', int)
GroupID = NewType('GroupID', int)


@dataclass
class User:
    user_id: UserID


@dataclass
class Group:
    group_id: GroupID
    name: str
