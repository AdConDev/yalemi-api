''' Table Model configuration with SQLModel '''

from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Column, Boolean, TIMESTAMP, text


class MayBase(SQLModel):
    ''' Defining the May Base Model '''
    title: str = Field(max_length=30, index=True, nullable=False)
    content: str = Field(max_length=150, index=True, nullable=False)
    published: bool | None = Field(
        sa_column=Column(
            Boolean(create_constraint=True),
            server_default='TRUE', nullable=False
        ),
    )


class MayCreate(MayBase):
    ''' Defining the May Crate Model '''


class MayRead(MayBase):
    ''' Defining the May Model '''
    id: int
    created_at: datetime


class MayUpdate(SQLModel):
    ''' Defining the May Update Model '''
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class May(MayBase, table=True):
    ''' Defining the May Model '''
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')),
        default=None)


class UserBase(SQLModel):
    ''' Defining the User Base Model '''
    nickname: str | None = Field(
        max_length=25, index=True, nullable=False)


class UserLogin(SQLModel):
    ''' Defining the User Login Model '''
    username: EmailStr = Field(nullable=False, unique=True)
    hashed_password: str = Field(max_length=512, nullable=False)


class UserUpdate(SQLModel):
    ''' Defining the User Update Model '''
    nickname: str | None = None
    username: EmailStr | None = None
    hashed_password: str | None = None
    enabled: bool | None = None


class UserCreate(UserBase, UserLogin):
    ''' Defining the User Create Model '''


class UserData(UserBase):
    ''' Defining the User Data Model '''
    username: EmailStr = Field(nullable=False)


class UserMetadata(SQLModel):
    ''' Defining the User Metadata Model '''
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')),
        default=None)
    enabled: bool | None = Field(
        sa_column=Column(
            Boolean(create_constraint=True),
            server_default='TRUE', nullable=False
        ),
    )


class UserRead(UserMetadata, UserData):
    ''' Defining the User Read Model '''


class User(UserRead, table=True):
    ''' Defining the User Model '''
    hashed_password: str = Field(max_length=512, nullable=False)


class Token(SQLModel):
    ''' Defining the Token Model '''
    access_token: str
    token_type: str


class TokenData(SQLModel):
    ''' Defining the Token Data Model '''
    username: str
