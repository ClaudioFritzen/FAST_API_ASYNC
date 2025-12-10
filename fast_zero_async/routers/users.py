from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero_async.database import get_session
from fast_zero_async.models import User
from fast_zero_async.schemas import (
    FilterPage,
    UserList,
    UserPublicSchema,
    UserSchema,
)
from fast_zero_async.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(tags=['Users Router'], prefix='/users')

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema, session: Session):

    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already registered',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already registered',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: Session,
    current_user: CurrentUser,
    filter_page: Annotated[FilterPage, Query()],
):

    users = session.scalars(
        select(User).offset(filter_page.skip).limit(filter_page.limit)
    ).all()
    return {'users': users}


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this user',
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already registered',
        )


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this user',
        )

    session.delete(current_user)
    session.commit()


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def read_user_by_id(user_id: int, session: Session):

    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db
