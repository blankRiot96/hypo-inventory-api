import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.core import router
from app.db.schema import get_session


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def get_test_session():
        yield session

    router.dependency_overrides[get_session] = get_test_session

    yield TestClient(router)

    router.dependency_overrides.clear()
