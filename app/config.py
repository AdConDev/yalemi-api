''' Responsible for managing the environment settings of application '''

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    ''' Represents the environment settings '''
    # Database settings
    dbms: str | None = None
    username: str | None = None
    password: str | None = None
    hostname: str | None = None
    port: str | None = None
    name: str | None = None
    # Secret key for the JWT token generation
    secret_key: str = ''
    # Algorithm for the JWT token generation
    algorithm: str = ''
    # Expiration time of the JWT token
    expire_minutes: int = 0

    class Config:
        ''' Specifies how environment variables should be read '''
        env_file = '.env'
        env_file_encoding = 'utf-8'

    def database_url(self) -> str:
        ''' Returns the database URL '''
        auth = f'{self.dbms}://{self.username}:{self.password}'
        url = f'{self.hostname}:{self.port}/{self.name}'
        return f'{auth}@{url}'
