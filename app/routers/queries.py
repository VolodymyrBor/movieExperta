import datetime as dt

from fastapi import APIRouter

from app.database.models import MovieInDB, DirectorInDB

router = APIRouter(tags=['queries'], prefix='/queries')


@router.get('/movie_range/{from_dt}/{to_dt}', response_model=list[MovieInDB])
async def get_movie_range(from_dt: dt.date, to_dt: dt.date) -> list[MovieInDB]:
    from_dt = dt.datetime.combine(from_dt, dt.time.min)
    to_dt = dt.datetime.combine(to_dt, dt.time.max)
    queryset = MovieInDB.find_many(
        MovieInDB.release_date >= from_dt,
        MovieInDB.release_date <= to_dt,
    )
    return await queryset.to_list()


@router.get('/movie_director_budget/{director_name}/{budget}', response_model=list[MovieInDB])
async def get_movies_by_director_and_budget(director_name: str, budget: float) -> list[MovieInDB]:
    queryset = MovieInDB.find_many(
        MovieInDB.director == director_name,
        MovieInDB.budget >= budget,
    )
    return await queryset.to_list()


@router.get(
    '/movie_director_country_or_len_related_movies/{director_country}/{len_related_movies}',
    response_model=list[MovieInDB],
)
async def get_movies_by_director_country_or_len_related_movies(
    director_country: str,
    len_related_movies: int,
) -> list[MovieInDB]:
    queryset = MovieInDB.find_all()
    all_movies = await queryset.to_list()
    filtered_movies = [
        movie
        for movie in all_movies
        if len(movie.related_movies) >= len_related_movies
    ]

    directors = [
        await DirectorInDB.find_one(DirectorInDB.name == movie.director)
        for movie in all_movies
    ]

    filtered_movies_by_directors = [
        movie
        for movie, director in zip(all_movies, directors)
        if director and director.country == director_country
    ]

    return filtered_movies + filtered_movies_by_directors
