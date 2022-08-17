from sqlmodel import select

from bantre.modules.article.article_model import Article
from bantre.system.user import User
from bantre.util.auth import get_user_by_username, verify_password

from .conftest import (
    Session,
    TestClient,
    User,
    admin_fixture,
    admin_user_password,
    admin_user_username,
    client_fixture,
    session_fixture,
)


def test_admin_fixture(session: Session, admin_user: User):
    admin_user_in_db = get_user_by_username(session, admin_user_username)
    assert admin_user_in_db == admin_user


def test_auth(session: Session, client: TestClient, admin_user: User):
    login_response = client.post(
        "/v1/auth/login",
        data={"username": admin_user_username, "password": admin_user_password},
    )

    assert login_response.status_code == 200
    login_json = login_response.json()
    print(login_json)

    refresh_response = client.post(
        "/v1/auth/refresh", json={"refresh_token": login_json["refresh_token"]}
    )
    print(refresh_response.json())
    assert refresh_response.status_code == 200
