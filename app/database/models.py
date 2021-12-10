from datetime import date
from beanie import Document

from app.database.engine import engine


@engine.register_model
class Director(Document):
    name: str


@engine.register_model
class Movie(Document):
    title: str
    releases_date: date
    budget: float
    related_movies: list[str]
