from fastapi.testclient import TestClient
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

client = TestClient(app=app)


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


def test_index():
    response = client.get(url="/")
    assert response.status_code == 200
    assert response.json() == {"message": f"Index Page"}


def test_health():
    response = client.get(url="/health")
    assert response.status_code == 200
    assert response.json() == {"message": f"Health OK"}


def test_add_fruit():
    response = client.post(
        url=f"/api/v1/fruits", json={"fruit": "Banana", "color": "Yellow"}
    )
    assert response.status_code == 201, response.text
    assert response.json() == {"message": f"New fruit has been added in the basket"}


def test_get_fruit():
    response = client.get(url=f"/api/v1/fruits/100")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["fruit"] == "Apple"
    assert data["color"] == "Red"
    assert data["id"] == 100


def test_get_fruits():
    response = client.get(url=f"/api/v1/fruits")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": 100, "fruit": "Apple", "color": "Red"},
        {"id": 101, "fruit": "Banana", "color": "Yellow"},
    ]


def test_update_fruit():
    fruit_id = 100
    response = client.put(
        url=f"/api/v1/fruits/{fruit_id}",
        json={"fruit": "Newfruit", "color": "Newcolor"},
    )
    assert response.status_code == 202, response.text
    assert response.json() == {
        "message": f"Fruit having fruit id: {fruit_id} has been updated"
    }


def test_delete_fruit():
    fruit_id = 100
    response = client.delete(url=f"/api/v1/fruits/{fruit_id}")
    assert response.status_code == 202, response.text
    assert response.json() == {
        "message": f"Fruit having fruit id: {fruit_id} has been deleted"
    }
    # Try to get the deleted item
    response_new = client.get(url=f"/api/v1/fruits/{fruit_id}")
    assert response_new.status_code == 404, response.text
