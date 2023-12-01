''' This file contains the functions that are used in the main files. '''

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> str:
    ''' Hashing the password '''
    return pwd_context.hash(password)
