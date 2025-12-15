from pydantic import BaseModel, EmailStr, Field

from fast_zero_async.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    username: str
    email: EmailStr
    id: int

    model_config = {
        'from_attributes': True,
    }


class UserList(BaseModel):
    users: list[UserPublicSchema]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    skip: int = Field(ge=0, default=0)
    limit: int = Field(ge=1, default=10)


class FilterName(FilterPage):
    name: str = Field(default='')


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
