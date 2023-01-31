
#Проверки реализованы в виде тестов на pytest (2 балла)

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm.session import Session as SessionBase, sessionmaker

from model_six_lesson import (
    User,
    Tag,
    Tag_Post,
    Post,
    Base
) 

from service_six_lesson import (
    create_user,
    create_users,
    create_tag,
    create_tags,
    create_post,
    get_tag_by_caption,
    get_posts_with_two_tags
)

from settings import TEST_DB_URL


TEST_USERNAME = "13-01-2023"
TEST_TAG_1 = 'tag3333'
TEST_POST = 'test_post'

@pytest.fixture(scope="session")
def engine():

    engine = create_engine(TEST_DB_URL)
    
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        pass


@pytest.fixture
def session(engine):

    Session = sessionmaker(bind = engine, autocommit = False)

    session = Session()
    session.autoflush = False
    return session
 
@pytest.fixture
def user():
    s = User(username = TEST_USERNAME, _password = 'pass')
    return s

      
@pytest.fixture
def tag():
    t = Tag(caption = TEST_TAG_1)
    return t

def test_get_user(session, user):
    with session.begin():
        session.add(user)
        session.flush()
        assert user == session.get(User, user.id)
        session.rollback()

def test_create_tag(session, tag):
        with session.begin():
            create_tag(session, tag.caption)
            session.flush()
            assert session.query(Tag).filter(Tag.caption == TEST_TAG_1).one_or_none() != None

def test_get_tag_by_caption(session, tag):
    with session.begin():
        test_tag = get_tag_by_caption(session, tag.caption)
        assert test_tag.caption == tag.caption

def test_get_user(session, user):
    with session.begin():
        session.add(user)
        session.flush()
        assert user == session.get(User, user.id)
        session.rollback()

def  test_create_post(session, user):
   
    with session.begin():
        session.add(user)
        session.flush()
        post = create_post(session, caption = TEST_POST, text = TEST_POST, user_id = user.id, tag_list = [TEST_TAG_1, "2", "3"])
        session.flush()
        assert post== session.query(Post).filter(Post.title == TEST_POST and Post.text == TEST_POST).one_or_none()
        session.rollback()

def test_get_post_with_2_tags(session, user):
    with session.begin():
        session.add(user)
        session.flush()
        post = create_post(session, caption = TEST_POST, text = TEST_POST, user_id = user.id, tag_list = [TEST_TAG_1, "2"])
        session.flush()
        post_with_2_tags = get_posts_with_two_tags(session, user.id)
        for item in post_with_2_tags:
            assert post.id in item
        session.rollback()