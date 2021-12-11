from fastapi import APIRouter
from beanie import PydanticObjectId

from app.database.models import CreateMovie, UpdateMovie, MovieInDB

router = APIRouter(tags=['movie'], prefix='/movies')


@router.put('/', response_model=MovieInDB)
async def create_movie(movie: CreateMovie) -> MovieInDB:
    movie_db = MovieInDB.parse_obj(movie)
    return await movie_db.insert()


@router.get('/{movie_id}', response_model=MovieInDB)
async def get_movie(movie_id: PydanticObjectId) -> MovieInDB:
    return await MovieInDB.get(movie_id)


@router.get('/', response_model=list[MovieInDB])
async def get_movies() -> list[MovieInDB]:
    return [movie async for movie in MovieInDB.find_all()]


@router.patch('/{movie_id}', response_model=MovieInDB)
async def update_movie(movie_id: PydanticObjectId, movie: UpdateMovie) -> MovieInDB:
    movie_db = await MovieInDB.get(movie_id)
    await movie_db.set(movie.dict(exclude_none=True))
    return movie_db
