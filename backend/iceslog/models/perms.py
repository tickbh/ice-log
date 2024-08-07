from datetime import datetime
from typing import Self
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, DateTime, func
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now

class PermsBase(SQLModel):
    id: int = Field(primary_key=True, description="id值")
    pid: int = Field(index=True, default=0, description="父id值")
    name: str = Field(max_length=50, nullable=False, description="名字")
    route: str = Field(max_length=255, nullable=False, description="路由")
    codename: str = Field(max_length=50, nullable=False, description="代码名字")
    status: int = Field(default=1, description="是否展示(1正常, 0禁用)")
    sort: int = Field(nullable=False, default=0, description="排序")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")

class Perms(PermsBase, table=True):
    pass

class GroupPermsBase(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int = Field(primary_key=True, description="ID")
    name: str = Field(max_length=50, nullable=False, description="名字")
    code: str = Field(max_length=50, nullable=False, description="代码")
    sort: int = Field(nullable=False, default=0, description="排序")
    status: int = Field(nullable=False, default=1, description="状态(1启用, 0禁用)")
    permissions: str = Field(max_length=10240, nullable=False, default="", description="拥有权限数,如 1, 2, 3, 4, 5")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")

class GroupPerms(GroupPermsBase, table=True):
    pass

class OnePerm(PermsBase):
    groups: str | None = None
    groups_name: str | None = None
    children: list[Self] = []
    
class PermsPublic(SQLModel):
    list: list[OnePerm]
    total: int
    
class GroupPermsPublic(SQLModel):
    list: list[GroupPermsBase]
    total: int