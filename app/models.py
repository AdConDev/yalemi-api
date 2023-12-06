''' Table Model configuration with SQLModel '''

from datetime import datetime
from typing import List
from pydantic import EmailStr
from sqlmodel import (
    Field, SQLModel, Column, Boolean, TIMESTAMP, text, Relationship
    )


class UserCreate(SQLModel):
    ''' Defining the User Create Model '''
    nickname: str | None = Field(max_length=25, nullable=True)
    username: str = Field(
        max_length=15, nullable=False, unique=True, index=True
        )
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(max_length=64, nullable=False)


class User(UserCreate, table=True):
    ''' Defining the User Model '''
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
    mayz: List['May'] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"}
        )


class UserMay(SQLModel):
    ''' Defining the User Data Model '''
    id: int | None = None
    nickname: str | None = None
    username: str | None = None
    enabled: bool | None = None


class UserUpdate(SQLModel):
    ''' Defining the User Update Model '''
    nickname: str | None = None
    username: str | None = None
    enabled: bool | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserRead(UserMay):
    ''' Defining the User Read Model '''
    created_at: datetime | None = None
    mayz: List['MayUser'] | None = None


class MayCreate(SQLModel):
    ''' Defining the May Create Model '''
    title: str = Field(max_length=30, index=True, nullable=False)
    content: str = Field(max_length=150, nullable=False)


class May(MayCreate, table=True):
    ''' Defining the May Model '''
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')
            ),
        default=None)
    likes: int | None = Field(default=0)
    user_id: int | None = Field(
        nullable=False,
        foreign_key='user.id',
        )
    user: User | None = Relationship(back_populates="mayz")


class MayUser(SQLModel):
    ''' Defining the May User Model '''
    id: int | None = None
    title: str | None = None
    content: str | None = None


class MayUpdate(SQLModel):
    ''' Defining the May Update Model '''
    title: str | None = None
    content: str | None = None


class MayRead(MayUser):
    ''' Defining the May Data Model '''
    created_at: datetime | None = None
    likes: int | None = None
    user: UserMay | None = None


class Token(SQLModel):
    ''' Defining the Token Model '''
    access_token: str
    token_type: str


class TokenData(SQLModel):
    ''' Defining the Token Data Model '''
    username: str
    email: str


UserRead.update_forward_refs()
