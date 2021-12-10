from typing import Type, TypeAlias, TypeVar

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from configs import config

DocumentType: TypeAlias = Type[Document]
DocumentT = TypeVar('DocumentT', bound=DocumentType)


class MongoEngine:

    def __init__(self, client: AsyncIOMotorClient | None = None):
        self._client = client
        self._models: list[DocumentType] = []

    @property
    def _connected_client(self) -> AsyncIOMotorClient:
        if self._client is None:
            raise ConnectionError('Connection is not created')
        return self._client

    async def connect(self):
        if self._client is None:
            self._client = AsyncIOMotorClient(str(config.MONGO.url))
        await init_beanie(
            database=self._connected_client[config.MONGO.DATABASE],
            document_models=self._models,
        )

    async def close(self):
        self._client.close()

    def register_model(self, model: DocumentT) -> DocumentT:
        self._models.append(model)
        return model


engine = MongoEngine()
