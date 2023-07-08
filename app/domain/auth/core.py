from dataclasses import dataclass
from typing import NewType

UserID = NewType('UserID', int)
GroupID = NewType('GroupID', int)


@dataclass
class User:
    user_id: UserID


class Group:
    group_id: GroupID
    name: str
    
    def __init__(self, group_id, name, *args, **kwargs):
        self.group_id = group_id
        self.name = name
