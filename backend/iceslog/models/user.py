from datetime import datetime, timezone
from pydantic import ConfigDict, EmailStr
from sqlalchemy import SMALLINT, BigInteger, DateTime, Integer, SmallInteger, func
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now
from iceslog.models.base import RetMsg

MIN_PASSWORD = 6
MAX_PASSWORD = 64

# Shared properties

class UserBase(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: EmailStr | None = Field(default=None, nullable=True, index=True, max_length=255)
    username: str = Field(unique=True, max_length=255)
    nickname: str | None = Field(default=None, nullable=True, max_length=255)
    status: int = Field(nullable=False, default=1, description="状态(1启用, 0禁用)")
    is_superuser: bool = False
    gender: int | None = Field(sa_column=SmallInteger,
        default=0, description="性别(1-男，2-女 0-未知)")
    user_type: str = Field(default=None, max_length=15,
                           description="用户类型, sys管理员")
    avatar: str | None = Field(
        default=None, max_length=255, description="用户头像")
    mobile: str | None = Field(
        default=None, max_length=15, unique=True, description="联系方式")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    create_by: int | None = Field(default=None, description="创建人id")
    update_time: datetime = Field(nullable=False, default_factory=datetime_now, description="更新时间")
    update_by: int | None = Field(default=None, description="更新人id")
    is_deleted: int = Field(default=0, description="逻辑删除标记")
    group_pem: int | None = Field(default=None, description="组权限id")

class UserCreate(UserBase):
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserRegister(SQLModel):
    username: EmailStr = Field(max_length=255)
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(
        default=None, max_length=255)  # type: ignore
    password: str | None = Field(
        default=None, min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(
        min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)
    new_password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    real_name: str | None = Field(
        default=None, max_length=255, description="实际名称")
    hashed_password: str
    
class UserEx(User):
    is_changed: bool = False

# Properties to return via API, id is always required

class UserMePublic(UserBase, RetMsg):
    id: int
    perms: list[str] | None
    
class UserPublic(UserBase, RetMsg):
    id: int
    
class MsgUserPublic(RetMsg):
    data: UserPublic

class UsersPublic(RetMsg):
    list: list[UserPublic]
    total: int
    
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
