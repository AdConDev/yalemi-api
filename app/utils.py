''' This file contains the functions that are used in the main files. '''

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    ''' Hashing the password '''
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    ''' Verifying the password '''
    return pwd_context.verify(plain_password, hashed_password)
