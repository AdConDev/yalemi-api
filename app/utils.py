''' Utility functions that are used across the application '''

# Import the passlib library and initiate the CryptContext class
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash a plain text password
def get_password_hash(password: str) -> str:
    ''' Takes a plain text password as input and returns a hashed version of
    the password. '''
    return pwd_context.hash(password)


# Function to verify whether the plain text password matches the hashed
# password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    ''' Verifies whether the plain text password matches the hashed
    password '''
    return pwd_context.verify(plain_password, hashed_password)
