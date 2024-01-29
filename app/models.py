''' Defines the data models for application and data base using SQLModel '''
# May stands for a kind of post in the application
from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import (
    Field, SQLModel, Column, Boolean, TIMESTAMP, text, Relationship,
    AutoString
    )


class VoteCreate(SQLModel):
    ''' Represents the data needed to create a new vote '''
    vote_type: int = Field(
        le=1, ge=-1, nullable=False, exclude=0
        )


class Vote(VoteCreate, table=True):
    ''' Represents a like, composed by a user and a May'''
    user_id: Optional[int] = Field(
        foreign_key="user.id", primary_key=True, nullable=False, default=None
    )
    may_id: Optional[int] = Field(
        foreign_key="may.id", primary_key=True, nullable=False, default=None
    )
    user: 'User' = Relationship(back_populates="may_votes")
    may: 'May' = Relationship(back_populates="user_votes")


class VoteRead(SQLModel):
    ''' Represents the data returned when reading a vote '''
    user: Optional['UserRel']
    may: Optional['MayRel']
    vote_type: Optional[int]


class VoteReadUsers(SQLModel):
    ''' Represents the data returned when reading a vote '''
    user: Optional['UserRel']
    vote_type: Optional[int]


class VoteReadMayz(SQLModel):
    ''' Represents the data returned when reading a vote '''
    may: Optional['MayRel']
    vote_type: Optional[int]


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
    may_votes: List['Vote'] = Relationship(back_populates="user")


class UserRel(SQLModel):
    ''' Represents a subset of the user data for May relationships '''
    id: Optional[int]
    nickname: Optional[str]
    username: Optional[str]
    enabled: Optional[bool]


class UserUpdate(SQLModel):
    ''' Represents the data needed to update an user '''
    nickname: Optional[str]
    username: Optional[str]
    enabled: Optional[bool]
    email: Optional[EmailStr]
    password: Optional[str]


class UserRead(UserRel):
    ''' Extends UserRel and represents the data returned when reading a
    user '''
    created_at: Optional[datetime]
    mayz: Optional[List['MayRel']]
    may_votes: Optional[List['VoteReadMayz']]


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
    user_id: Optional[int] = Field(
        foreign_key='user.id',
        default=None,
        nullable=False
        )
    user: User = Relationship(back_populates="mayz")
    user_votes: List['Vote'] = Relationship(back_populates="may")


class MayRel(SQLModel):
    ''' Represents a subset of the May data for User relationships '''
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]


class MayUpdate(SQLModel):
    ''' Represents the data needed to update a May '''
    title: Optional[str]
    content: Optional[str]


class MayRead(MayRel):
    ''' Extends MayRel and represents the data returned when reading a May '''
    created_at: Optional[datetime]
    user: Optional[UserRel]
    user_votes: Optional[List['VoteReadUsers']]


class Token(SQLModel):
    ''' Represents a token '''
    access_token: str
    token_type: str


class TokenData(SQLModel):
    ''' Represents the data in a token '''
    username: Optional[str]
    email: Optional[str]


# Update forward references, which is necessary because of the circular
# references between the User and May classes.
UserRead.model_rebuild()
MayRead.model_rebuild()
VoteRead.model_rebuild()
