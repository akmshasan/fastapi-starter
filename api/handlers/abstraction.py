from sqlalchemy.orm import Session

from api.database.models import DBFruit
from api.schemas.schemas import Fruit, FruitCreate, FruitUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    return (
        db.query(DBFruit)
        .group_by(DBFruit.id)
        .filter(DBFruit.fruit.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )


def create(db: Session, fruit: FruitCreate):
    db_fruit = DBFruit(**fruit.model_dump())
    db.add(db_fruit)
    db.commit()
    db.refresh(db_fruit)
    return db_fruit


def get_by_id(db: Session, fruit_id: int):
    return db.query(DBFruit).filter(DBFruit.id == fruit_id).first()


def update(db: Session, fruit_id: int, update_parameter: FruitUpdate):
    db_fruit = get_by_id(db=db, fruit_id=fruit_id)
    for key, value in update_parameter.model_dump().items():
        setattr(db_fruit, key, value)
    db.commit()
    db.refresh(db_fruit)
    return Fruit(**db_fruit.__dict__)


def delete(db: Session, fruit: Fruit):
    db.delete(fruit)
    db.commit()
    return fruit
