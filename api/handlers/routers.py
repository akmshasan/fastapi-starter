from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.database.models import DBFruit
from api.schemas.schemas import Fruit, FruitCreate, FruitUpdate

router = APIRouter(prefix="/api/v1/fruits", tags=["Fruits"])


@router.post(
    path="/",
    status_code=201,
)
async def add_fruit(new_fruit: FruitCreate, db: Session = Depends(get_db)) -> Fruit:
    db_fruit = DBFruit(**new_fruit.model_dump())
    db.add(db_fruit)
    db.commit()
    db.refresh(db_fruit)
    return Fruit(**db_fruit.__dict__)


@router.get(
    path="/",
    status_code=200,
)
async def get_fruits(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
) -> List[Fruit]:
    skip = (page - 1) * limit
    fruit_list = (
        db.query(DBFruit)
        .group_by(DBFruit.id)
        .filter(DBFruit.fruit.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return fruit_list


@router.get(
    path="/{fruit_id}",
    status_code=200,
)
async def get_fruit_by_id(fruit_id: int, db: Session = Depends(get_db)) -> Fruit:
    expected_fruit = db.query(DBFruit).filter(DBFruit.id == fruit_id).first()
    return expected_fruit


@router.put(
    path="/{fruit_id}",
    status_code=202,
)
def update_fruit(
    fruit_id: int, update_fruit: FruitUpdate, db: Session = Depends(get_db)
) -> Fruit:
    db_fruit = db.query(DBFruit).filter(DBFruit.id == fruit_id).first()
    if db_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")
    for key, value in update_fruit.model_dump().items():
        setattr(db_fruit, key, value)
    db.commit()
    db.refresh(db_fruit)
    return Fruit(**db_fruit.__dict__)


@router.delete(
    path="/{fruit_id}",
    status_code=202,
)
def delete_fruit(fruit_id: int, db: Session = Depends(get_db)) -> Fruit:
    db_fruit = db.query(DBFruit).filter(DBFruit.id == fruit_id).first()
    if db_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")
    db.delete(db_fruit)
    db.commit()
    return Fruit(**db_fruit.__dict__)
