from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, or_, select

from iceslog import cruds
from iceslog.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash, verify_password
from iceslog.models import (
    RetMsg,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from iceslog.models.user import MsgUserMePublic, MsgUserPublic, MsgUsersPublic, UserMePublic
from iceslog.utils import cache_utils, generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/page",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MsgUsersPublic,
)
def read_users(session: SessionDep, pageNum: int = 0, pageSize: int = 100, key: str = None, is_active: bool = None, startTime: str = None, endTime: str = None) -> Any:
    """
    Retrieve users.
    """
    statement = select(User)
    if key:
        statement = statement.where(or_(User.username.like(f"%{key}%"), User.nickname.like(f"%{key}%"), User.mobile.like(f"%{key}%")))
    
    if is_active != None:
        statement = statement.where(User.is_active == is_active)
    
    if startTime:
        statement = statement.where(User.create_time__gt == startTime)
    
    if endTime:
        statement = statement.where(User.create_time__lt == endTime)
        
    # count1 = session.exec(statement).one_or_none()
    
    # statement = select(User).where(User.username.like("a%"))
    # count2 = session.exec(statement).one_or_none()

    # count_statement = select(func.count()).select_from(User)
    # count_statement = select(func.count()).from_statement(statement)
    
    # count = session.exec(count_statement).one()
    count = session.exec(statement).all().count()

    statement = statement.offset((pageNum - 1) * pageSize).limit(pageSize)
    users = session.exec(statement).all()

    return MsgUsersPublic(data = UsersPublic(list=users, total=count)) 

@router.get(
    "/form", 
    dependencies=[Depends(get_current_active_superuser)], 
    response_model=MsgUserPublic
)
def read_user_form(*, session: SessionDep, user_id: int) -> Any:
    
    user = session.get(User, user_id)
    if not user:
        return RetMsg("00001", "账号不存在")
    
    return MsgUserPublic(data = user)


@router.get("/me", response_model=MsgUserMePublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    me = UserMePublic.model_validate(current_user, update={"perms": []})
    me.perms = cache_utils.get_all_perms(current_user.group_pem)
    return MsgUserMePublic(data=me)

@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = cruds.user.get_user_by_username(session=session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = cruds.user.create_user(session=session, user_create=user_in)
    # if settings.emails_enabled and user_in.email:
    #     email_data = generate_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    #     send_email(
    #         email_to=user_in.email,
    #         subject=email_data.subject,
    #         html_content=email_data.html_content,
    #     )
    return user


# @router.patch("/me", response_model=UserPublic)
# def update_user_me(
#     *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
# ) -> Any:
#     """
#     Update own user.
#     """

#     if user_in.email:
#         existing_user = crud.get_user_by_email(session=session, email=user_in.email)
#         if existing_user and existing_user.id != current_user.id:
#             raise HTTPException(
#                 status_code=409, detail="User with this email already exists"
#             )
#     user_data = user_in.model_dump(exclude_unset=True)
#     current_user.sqlmodel_update(user_data)
#     session.add(current_user)
#     session.commit()
#     session.refresh(current_user)
#     return current_user


# @router.patch("/me/password", response_model=RetMsg)
# def update_password_me(
#     *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
# ) -> Any:
#     """
#     Update own password.
#     """
#     if not verify_password(body.current_password, current_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect password")
#     if body.current_password == body.new_password:
#         raise HTTPException(
#             status_code=400, detail="New password cannot be the same as the current one"
#         )
#     hashed_password = get_password_hash(body.new_password)
#     current_user.hashed_password = hashed_password
#     session.add(current_user)
#     session.commit()
#     return RetMsg(message="Password updated successfully")



# @router.get("/page", response_model=MsgUserPublic)
# def read_user_me(current_user: CurrentUser) -> Any:
#     """
#     Get current user.
#     """
#     return MsgUserPublic(data=current_user)

# @router.delete("/me", response_model=RetMsg)
# def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
#     """
#     Delete own user.
#     """
#     if current_user.is_superuser:
#         raise HTTPException(
#             status_code=403, detail="Super users are not allowed to delete themselves"
#         )
#     statement = delete(Item).where(col(Item.owner_id) == current_user.id)
#     session.exec(statement)  # type: ignore
#     session.delete(current_user)
#     session.commit()
#     return RetMsg(message="User deleted successfully")


# @router.post("/signup", response_model=UserPublic)
# def register_user(session: SessionDep, user_in: UserRegister) -> Any:
#     """
#     Create new user without the need to be logged in.
#     """
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail="Open user registration is forbidden on this server",
#         )
#     user = crud.get_user_by_email(session=session, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this email already exists in the system",
#         )
#     user_create = UserCreate.model_validate(user_in)
#     user = crud.create_user(session=session, user_create=user_create)
#     return user


# @router.get("/{user_id}", response_model=UserPublic)
# def read_user_by_id(
#     user_id: int, session: SessionDep, current_user: CurrentUser
# ) -> Any:
#     """
#     Get a specific user by id.
#     """
#     user = session.get(User, user_id)
#     if user == current_user:
#         return user
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail="The user doesn't have enough privileges",
#         )
#     return user


@router.put(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MsgUserPublic,
)
def update_user(
    *,
    session: SessionDep,
    user_id: int,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = cruds.user.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = cruds.user.update_user(session=session, db_user=db_user, user_in=user_in)
    return MsgUserPublic(data=db_user)


# @router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
# def delete_user(
#     session: SessionDep, current_user: CurrentUser, user_id: int
# ) -> RetMsg:
#     """
#     Delete a user.
#     """
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if user == current_user:
#         raise HTTPException(
#             status_code=403, detail="Super users are not allowed to delete themselves"
#         )
#     statement = delete(Item).where(col(Item.owner_id) == user_id)
#     session.exec(statement)  # type: ignore
#     session.delete(user)
#     session.commit()
#     return RetMsg(message="User deleted successfully")
