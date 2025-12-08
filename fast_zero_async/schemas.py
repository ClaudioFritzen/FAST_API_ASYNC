from pydantic import BaseModel, EmailStr


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
