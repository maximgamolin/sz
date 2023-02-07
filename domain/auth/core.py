from dataclasses import dataclass


@dataclass
class User:
    user_id: int


@dataclass
class Group:
    group_id: int
    name: str
    users: list[User]
