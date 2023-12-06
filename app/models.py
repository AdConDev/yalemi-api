''' Table Model configuration with SQLModel '''

from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Column, Boolean, TIMESTAMP, text


class MayData(SQLModel):
    ''' Defining the May Data Model '''
    title: str = Field(max_length=30, index=True, nullable=False)
    content: str = Field(max_length=150, nullable=False)
    published: bool | None = Field(
        sa_column=Column(
            Boolean(create_constraint=True),
            server_default='TRUE', nullable=False
            ),
        )


class MayMetadata(SQLModel):
    ''' Defining the May Metadata Model '''
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')
            ),
        default=None)
    user_id: int | None = Field(nullable=False, foreign_key='user.id')
    likes: int | None = Field(default=0)


class MayCreate(MayData):
    ''' Defining the May Create Model '''


class MayRead(MayData, MayMetadata):
    ''' Defining the May Model '''


class MayUpdate(SQLModel):
    ''' Defining the May Update Model '''
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class May(MayRead, table=True):
    ''' Defining the May Model '''


class UserBase(SQLModel):
    ''' Defining the User Base Model '''
    nickname: str = Field(max_length=25, nullable=False)


class UserUpdate(SQLModel):
    ''' Defining the User Update Model '''
    nickname: str | None = None
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    enabled: bool | None = None


class UserCreate(UserBase):
    ''' Defining the User Create Model '''
    username: str = Field(
        max_length=15, nullable=False, unique=True, index=True)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(max_length=512, nullable=False)


class UserData(UserBase):
    ''' Defining the User Data Model '''
    username: str = Field(
        max_length=15, nullable=False, unique=True, index=True)
    email: EmailStr = Field(nullable=False, unique=True, index=True)


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
    password: str = Field(max_length=64, nullable=False)


class Token(SQLModel):
    ''' Defining the Token Model '''
    access_token: str
    token_type: str


class TokenData(SQLModel):
    ''' Defining the Token Data Model '''
    username: str
