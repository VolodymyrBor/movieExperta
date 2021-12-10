from fastapi import FastAPI

from app.routers import router
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
    app.include_router(router=router)
    return app
