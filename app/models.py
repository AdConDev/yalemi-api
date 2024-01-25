''' Defines the data models for application and data base using SQLModel '''
# May stands for a kind of post in the application
from datetime import datetime
from typing import List, Optional
from enum import IntEnum
from sqlalchemy_utils import ChoiceType
from pydantic import EmailStr
from sqlmodel import (
    Field, SQLModel, Column, Boolean, TIMESTAMP, text, Relationship,
    AutoString, Integer
    )


class VoteType(IntEnum):
    ''' Represents the type of vote '''
    UP = 1
    DOWN = -1


class VoteCreate(SQLModel):
    ''' Represents the data needed to create a new vote '''
    may_id: int = Field(
        foreign_key="may.id", primary_key=True, nullable=False
    )
    vote_type: VoteType = Field(
        sa_column=Column(ChoiceType(VoteType, impl=Integer()), nullable=False)
        )


class Vote(VoteCreate, table=True):
    ''' Represents a like, composed by a user and a May'''
    user_id: int = Field(
        foreign_key="user.id", primary_key=True, nullable=False
    )


class UserCreate(SQLModel):
    ''' Represents the data needed to create a new user '''
    nickname: str = Field(max_length=25, nullable=False)
    username: str = Field(
        max_length=15, nullable=False, unique=True, index=True
        )
    email: EmailStr = Field(nullable=False, unique=True, sa_type=AutoString)
    password: str = Field(max_length=64, nullable=False)


class User(UserCreate, table=True):
    ''' Extends UserCreate and represents a user in the database '''
    id: Optional[int] = Field(primary_key=True, default=None)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')
            ),
        default=None
        )
    enabled: Optional[bool] = Field(
        sa_column=Column(
            Boolean(create_constraint=True),
            server_default='TRUE',
            nullable=False
        ),
        default=None
    )
    mayz: List['May'] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"}
        )


class UserMay(SQLModel):
    ''' Represents a subset of the user data for May relationships '''
    id: int | None = None
    nickname: str | None = None
    username: str | None = None
    enabled: bool | None = None


class UserUpdate(SQLModel):
    ''' Represents the data needed to update an user '''
    nickname: str | None = None
    username: str | None = None
    enabled: bool | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserRead(UserMay):
    ''' Extends UserMay and represents the data returned when reading a
    user '''
    created_at: datetime | None = None
    mayz: List['MayUser'] | None = None


class MayCreate(SQLModel):
    ''' Represents the data needed to create a new May '''
    title: str = Field(max_length=30, nullable=False)
    content: str = Field(max_length=150, nullable=False)


class May(MayCreate, table=True):
    ''' Extends MayCreate and represents a May in the database '''
    id: Optional[int] = Field(primary_key=True, default=None)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')
            ),
        default=None
        )
    likes: Optional[int] = Field(default=0, nullable=False)
    user_id: Optional[int] = Field(
        foreign_key='user.id',
        default=None,
        nullable=False
        )
    user: User = Relationship(back_populates="mayz")


class MayUser(SQLModel):
    ''' Represents a subset of the May data for User relationships '''
    id: int | None = None
    title: str | None = None
    content: str | None = None


class MayUpdate(SQLModel):
    ''' Represents the data needed to update a May '''
    title: str | None = None
    content: str | None = None


class MayRead(MayUser):
    ''' Extends MayUser and represents the data returned when reading a May '''
    created_at: datetime | None = None
    likes: int | None = None
    user: Optional[UserMay] = None


class Token(SQLModel):
    ''' Represents a token '''
    access_token: str
    token_type: str


class TokenData(SQLModel):
    ''' Represents the data in a token '''
    username: str | None
    email: str | None


# Update forward references, which is necessary because of the circular
# references between the User and May classes.
UserRead.model_rebuild()
MayRead.model_rebuild()
