import pytest

from bantre.system.user import User

from .conftest import Session, client_fixture, session_fixture


@pytest.mark.unit
def test_user_orm(session: Session):
    # Create user using the orm
    post_user = User(username="bucky", email="ricky@bucky.com", password="timini")
    session.add(post_user)
    session.commit()
    session.refresh(post_user)
    # Assert that the posted user now has an id
    assert post_user.id is not None

    # Get the same user from the orm
    get_user = session.get(User, post_user.id)
    assert get_user.id == post_user.id
    assert get_user.username == "bucky"
    assert get_user.password == "timini"
    assert get_user.email == "ricky@bucky.com"

    # Update the users username
    get_user.username = "ricky"
    session.add(get_user)
    session.commit()

    # Assert that users username is really updated
    updated_user = session.get(User, post_user.id)
    assert updated_user.username == "ricky"

    # Delete the user
    session.delete(get_user)
    session.commit()

    # Assert that it really is deleted
    deleted_user = session.get(User, post_user.id)
    assert deleted_user is None


# def test_create_user(client: TestClient): # Navnene på variablene må være det samme som står i pytest.fixture dekoratorene
#     # This will be boilerplate for running tests using endpoints
#     # Create user
#     response = client.post(
#         "/v1/users", json= {
#             "username": "bucky",
#             "name": "Richard-Andre Hewlett Buckminister Fuller",
#             "email": "ricky@bucky.com",
#             "private_email": "ladiesman@gmail.com",
#             "birthday": "2006-09-10",
#             "phone": "12345678"
#         }
#     )
#     data = response.json()

#     # Assert that he is equal to the one that we created
#     assert response.status_code == 200
#     assert data["name"] == "Richard-Andre Hewlett Buckminister Fuller"
#     assert data["email"] == "ricky@bucky.com"
#     assert data["private-email"] == "ladiesman@gmail.com"
#     assert data["birthday"] == "2006-09-10"
