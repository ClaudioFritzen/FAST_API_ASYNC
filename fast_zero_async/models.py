from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), init=False, server_default=func.now()
    )

    todos: Mapped[list['Todo']] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    state: Mapped[TodoState] = mapped_column(
        SqlEnum(TodoState, name='todo_state'), default=TodoState.draft
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), init=False, server_default=func.now()
    )
