from typing import Optional

from pydantic import BaseModel


class Fruit(BaseModel):
    id: int
    fruit: str
    color: str


class FruitCreate(BaseModel):
    fruit: str = "Enter a fruit name"
    color: str = "Enter the color"


class FruitUpdate(BaseModel):
    fruit: Optional[str] = None
    color: Optional[str] = None
