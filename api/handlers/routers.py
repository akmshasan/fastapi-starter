from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.database.models import DBFruit
from api.handlers.abstraction import create, get_all, get_by_id, delete, update
from api.schemas.schemas import Fruit, FruitCreate, FruitUpdate

router = APIRouter(prefix="/api/v1/fruits", tags=["Fruits"])


@router.post(
    path="/",
    status_code=201,
    response_model=Fruit,
)
async def add_fruit(fruit: FruitCreate, db: Session = Depends(get_db)) -> Fruit:
    db_fruit: Fruit = create(db=db, fruit=fruit)
    return db_fruit


@router.get(
    path="/",
    status_code=200,
    response_model=list[Fruit],
)
async def get_fruits(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
) -> list[Fruit]:
    skip: int = (page - 1) * limit
    fruit_list: list = get_all(db=db, limit=limit, skip=skip, search=search)
    return fruit_list


@router.get(
    path="/{fruit_id}",
    status_code=200,
    response_model=Fruit,
)
async def get_fruit(fruit_id: int, db: Session = Depends(get_db)) -> Fruit:
    expected_fruit: Fruit = get_by_id(db=db, fruit_id=fruit_id)
    if expected_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return expected_fruit


@router.put(
    path="/{fruit_id}",
    status_code=202,
    response_model=Fruit,
)
def update_fruit(
    fruit_id: int, update_fruit: FruitUpdate, db: Session = Depends(get_db)
) -> Fruit:
    db_fruit = get_by_id(db=db, fruit_id=fruit_id)
    if db_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return update(db=db, update_parameter=update_fruit, fruit_id=fruit_id)


@router.delete(
    path="/{fruit_id}",
    status_code=202,
    response_model=Fruit,
)
def delete_fruit(fruit_id: int, db: Session = Depends(get_db)) -> Fruit:
    db_fruit: Fruit = get_by_id(db=db, fruit_id=fruit_id)
    if db_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return delete(db=db, fruit=db_fruit)
