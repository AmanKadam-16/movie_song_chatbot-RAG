from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from movie_assistant.schemas.app_enums import Role


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr = Field(...)


class AddUser(UserBase):
    password: str = Field(..., min_length=8)


class GetUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class GetUserInfo(UserBase):
    id: uuid4
    role: Role


class LoginResponse(UserBase):
    token_type: str = "access"
    token: str = Field(...)
