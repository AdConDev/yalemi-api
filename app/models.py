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
    username: str | None = Field(max_length=25, index=True, nullable=False)
    email: EmailStr = Field(unique=True, index=True, nullable=False)


class UserCreate(UserBase):
    ''' Defining the User Create Model '''
    password: str = Field(max_length=128, nullable=False)


class UserRead(UserBase):
    ''' Defining the User Read Model '''
    id: int
    created_at: datetime


class UserUpdate(SQLModel):
    ''' Defining the User Update Model '''
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class User(UserCreate, table=True):
    ''' Defining the User Model '''
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('NOW()')),
        default=None)
