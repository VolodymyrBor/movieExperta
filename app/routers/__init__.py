from . import movie, director, queries

__routers__ = [
    movie.router,
    director.router,
    queries.router,
]
