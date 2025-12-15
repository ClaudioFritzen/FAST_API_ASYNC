from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero_async.database import get_session
from fast_zero_async.models import Todo, User
from fast_zero_async.schemas import TodoPublic, TodoSchema
from fast_zero_async.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=list[TodoPublic])
async def todos(
    user: CurrentUser,
    session: Session,
):
    result = await session.scalars(select(Todo).where(Todo.user_id == user.id))
    return result.all()


@router.post('/', response_model=TodoPublic)
async def criar_new_task(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo
