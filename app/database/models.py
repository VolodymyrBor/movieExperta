import datetime as dt
from decimal import Decimal
from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, validator

from app.database.engine import engine


class CreateDirector(BaseModel):
    name: str
    birthday: dt.date
    country: str


class UpdateDirector(CreateDirector):
    name: Optional[str] = None
    birthday: Optional[dt.date] = None
    country: Optional[str] = None


@engine.register_model
class DirectorInDB(Document, CreateDirector):
    birthday: dt.datetime

    @validator('birthday', pre=True)
    def _to_datetime(cls, value: Any) -> dt.datetime:
        if isinstance(value, dt.date):
            return dt.datetime.combine(value, dt.time.min)
        return value

    class Config:
        orm_mode = True


class CreateMovie(BaseModel):
    title: str
    release_date: dt.date
    budget: Decimal
    related_movies: list[str] = []
    director: str


class UpdateMovie(BaseModel):
    title: Optional[str] = None
    release_date: Optional[dt.date] = None
    budget: Optional[Decimal] = None
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
