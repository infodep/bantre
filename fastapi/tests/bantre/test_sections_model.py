from bantre.system.group import Group, GroupSectionLink
from bantre.system.section import Section

from .conftest import Session, client_fixture, session_fixture


def test_section_orm(session: Session):
    post_group = Group(
        name="timinister",
        description="Gruppe for alle timinister",
        type=1,
    )
    post_section = Section(
        name="test_section",
        description="section made for test",
    )
    post_group_section_link = GroupSectionLink(
        group=post_group, section=post_section, read=True, write=False, admin=False
    )
    session.add(post_group)
    session.add(post_section)
    session.add(post_group_section_link)
    session.commit()

    # Make sure group and section really are linked
    groups_in_section_from_db = []
    for link in post_section.groups_permissions:
        groups_in_section_from_db.append(link.group)

    assert post_group in groups_in_section_from_db
