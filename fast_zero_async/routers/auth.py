from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero_async.database import get_session
from fast_zero_async.models import User
from fast_zero_async.schemas import TokenSchema, LoginSchema
from fast_zero_async.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(tags=['Auth Router'], prefix='/auth')

Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[AsyncSession, Depends(get_current_user)]


@router.post('/token', response_model=TokenSchema, status_code=HTTPStatus.OK)
async def get_token(
    form_data: OAuth2Form,
    session: Session,
):

    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    ascess_token = create_access_token(data={'sub': user.email})
    return {'access_token': ascess_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=TokenSchema)
async def refresh_access_token(
    user: CurrentUser,
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}


@router.post('/login', status_code=HTTPStatus.OK)
async def login(
    user: LoginSchema,
    session: Session
):
    # Implement login logic here
    user_db = await session.scalar(
        select(User).where(User.email == user.email)

    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(user.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Create access token
    ascess_token = create_access_token(data={'sub': user.email})

    return {
        "message": f"User {user.email} logged in successfully",
        "access_token": ascess_token,
        "token_type": "bearer"
    }
    

@router.post('/logout', status_code=HTTPStatus.OK)
async def logout(
    user: CurrentUser,
):
    # Implement logout logic here
    return {'message': f'User {user.email} logged out successfully'}