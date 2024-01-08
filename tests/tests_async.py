import pytest
from httpx import AsyncClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from api.database.database import Base, get_db
from api.database.models import DBFruit
from api.main import app

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)

    # Create test item
    session = TestingSessionLocal()
    db_fruit = DBFruit(id=100, fruit="Apple", color="Red")
    session.add(db_fruit)
    session.commit()
    session.close()


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)


@pytest.mark.anyio
async def test_index():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": f"Index Page"}


@pytest.mark.anyio
async def test_health():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": f"Health OK"}
