import datetime as dt
from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, validator

from app.database.engine import engine


@engine.register_model
class Director(Document):
    name: str


class CreateMovie(BaseModel):
    title: str
    release_date: dt.date
    budget: float
    related_movies: list[str] = []
    director: str


class UpdateMovie(BaseModel):
    title: Optional[str] = None
    release_date: Optional[dt.date] = None
    budget: Optional[float] = None
    related_movies: Optional[list[str]] = None
    director: Optional[str] = None


@engine.register_model
class MovieInDB(Document, CreateMovie):
    release_date: dt.datetime

    @validator('release_date', pre=True)
    def _to_datetime(cls, value: Any) -> dt.datetime:
        if isinstance(value, dt.date):
            return dt.datetime.combine(value, dt.time.min)
        return value

    class Config:
        orm_mode = True
