from bantre.system.group import Group
from bantre.system.user import User

from .conftest import Session, client_fixture, session_fixture


def test_group_orm(session: Session):
    # Create user and group using the orm
    post_user = User(username="bucky", email="ricky@bucky.com", password="timini")
    post_group = Group(
        name="timinister", description="Gruppe for alle timinister", type=1
    )
    session.add(post_user)
    session.add(post_group)
    session.commit()
    session.refresh(post_user)
    session.refresh(post_group)

    # Add the group to the user
    post_user.groups.append(post_group)
    session.add(post_user)
    session.commit()
    session.refresh(post_user)
    session.refresh(post_group)

    # Check that user is in group from both ends
    assert post_user in post_group.members
    assert post_group in post_user.groups

    # Make sure that deleting user doesnt delete group
    session.delete(post_user)
    session.commit()
    session.refresh(post_group)

    assert post_group.members == []
