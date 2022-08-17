import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from bantre.app import app
from bantre.database import get_session
from bantre.system.user import User
from bantre.util.auth import hash_password


admin_user_username: str = "admin"
admin_user_password: str = "adminpass"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_user")
def admin_fixture(session: Session):
    hashed_password = hash_password(admin_user_password)
    admin_user = User(
        username=admin_user_username, email="admin@timini.no", password=hashed_password
    )
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    try:
        yield admin_user
    finally:
        session.delete(admin_user)
        session.commit()
