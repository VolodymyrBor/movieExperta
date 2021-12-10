from fastapi import APIRouter

from app.database.models import Movie

router = APIRouter(tags=['movie'], prefix='/movies')


@router.post('/', response_model=Movie)
async def create_movie(movie: Movie) -> Movie:
    await movie.insert()
    return movie
