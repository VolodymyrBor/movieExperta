from fastapi import APIRouter
from beanie import PydanticObjectId

from app.database.models import CreateDirector, DirectorInDB, UpdateDirector

router = APIRouter(tags=['director'], prefix='/directors')


@router.put('/', response_model=DirectorInDB)
async def create_director(director: CreateDirector) -> DirectorInDB:
    director_db = DirectorInDB.parse_obj(director)
    return await director_db.insert()


@router.get('/{director_id}', response_model=DirectorInDB)
async def get_director(director_id: PydanticObjectId) -> DirectorInDB:
    return await DirectorInDB.get(director_id)


@router.get('/', response_model=list[DirectorInDB])
async def get_directors() -> list[DirectorInDB]:
    return [director async for director in DirectorInDB.find_all()]


@router.patch('/{director_id}', response_model=DirectorInDB)
async def update_director(director_id: PydanticObjectId, director: UpdateDirector) -> DirectorInDB:
    director_db = await DirectorInDB.get(director_id)
    await director_db.set(director.dict(exclude_none=True))
    return director_db
