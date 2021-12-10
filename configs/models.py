from pydantic import BaseModel

from url import URL


class MongoConfig(BaseModel):
    HOST: str = 'localhost'
    PORT: int = 27017
    USERNAME: str = 'root'
    PASSWORD: str = 'root'
    DATABASE: str = 'default_db'

    @property
    def url(self) -> URL:
        return URL(
            scheme='mongodb',
            host=self.HOST,
            port=self.PORT,
            username=self.USERNAME,
            password=self.PASSWORD,
        )


class Config(BaseModel):
    MONGO: MongoConfig = MongoConfig()

    HOST: str = 'localhost'
    PORT: int = 8000
    RELOAD: bool = False
