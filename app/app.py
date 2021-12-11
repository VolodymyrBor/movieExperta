from fastapi import FastAPI

from app.routers import __routers__
from app.database.engine import engine


def create_app() -> FastAPI:
    app = FastAPI(
        on_startup=[
            engine.connect,
        ],
        on_shutdown=[
            engine.close,
        ],
    )
    for router in __routers__:
        app.include_router(router)
    return app
