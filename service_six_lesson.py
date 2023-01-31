
from sqlalchemy import (
    create_engine,
    func
)

from sqlalchemy.orm import (
    declarative_base,
    Session as SessionType,
    sessionmaker,
    scoped_session,
)

from model_six_lesson import (
    User,
    Tag,
    Post,
    Tag_Post
)
from datetime import datetime

from settings import DB_URL


engine = create_engine(url=DB_URL)
Base = declarative_base(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base.metadata.create_all()
session: SessionType = Session()

def create_user(session: SessionType, username: str, password: str) -> User:
    user = User(username=username, _password = password)
    session.add(user)
    return user


def create_users(session: SessionType, *usernames: str) -> list[User]:
    users = []
    for username in usernames:
        user = User(username=username)
        session.add(user)
        users.append(user)

    return users


def get_all_users(session: SessionType) -> list[User]:
    users = session.query(User).order_by(User.id).all()
    return users


def get_user_by_username(session: SessionType, username: str) -> User | None:
    user = session.query(User).filter_by(username=username).one_or_none()
    return user


def get_user_by_id(session: SessionType, user_id: int) -> User | None:
    user = session.get(User, user_id)
    return user

def get_users_by_username_match(session: SessionType, username_part: str) -> list[User]:
    users = session.query(User).filter(User.username.ilike(f"%{username_part}%")).all()
    return users

def update_username_by_id(session: SessionType, user_id, new_username) -> User | None:
    user = session.get(User, user_id)
    user.username = new_username
    session.add(user)
    session.flush()
    return user

def get_tag_by_caption(session: SessionType, caption: str) -> Tag | None:
    tag = session.query(Tag).filter(Tag.caption == caption).first()
    return tag

def create_tag(session: SessionType, caption: str) -> Tag:
    
    existed_tag = get_tag_by_caption(session, caption)

    if not existed_tag is None:
        return existed_tag
    else:
        tag= Tag(caption=caption)
        session.add(tag)
        return tag

    

def create_tags(session: SessionType, captions) -> list[Tag]:
    tags = []
    for caption in captions:
        tag = create_tag(session, caption)
        tags.append(tag)

    return tags



def get_tag_by_id(session: SessionType, tag_id: str) -> Tag | None:
    tag = session.get(Tag, tag_id)
    return tag

def create_post(session: SessionType, caption: str, text: str, user_id: int, tag_list : list[str]) -> Post | None:
    post = Post(title=caption, text = text, user_id = user_id)
    session.add(post)
    

    if tag_list != []:
         tags = []
         for caption in tag_list:
                tag = create_tag(session, caption)
                tags.append(tag)

         post.tags = tags
        
    return post

def update_post_by_id(session : Session, post_id : int) -> Post | None:
    post = session.get(Post, post_id)
    session.add(post)
    return post


def get_posts_by_user_id (session : Session, user_id : int) -> list[Post]:
    posts = session.query(Post).filter(Post.user_id ==user_id).all()
    return posts

def get_posts_by_tag_id(session : Session, tag_id : int) -> list[Post]:
    posts = session.query(Post).filter(Post.tags == tag_id).all()
    return posts

#Выбрать все посты конкретного пользователя с 2-мя любыми тегами
def get_posts_with_two_tags(session : Session, user_id : int) -> list[int] | None:
    query= session.query(Tag_Post.post_id).join(Post).where(Post.user_id == user_id).group_by(Tag_Post.post_id).having(func.count(Tag_Post.tag_id) == 2)
    post_ids = []
    post_ids = query.all()
    
    return post_ids


#Добавить некоторые данные.
def main():

    username  = str(datetime.now())
    Base.metadata.drop_all()
    Base.metadata.create_all()

    with session.begin():
        create_user(session, username, "123")
        create_tags(session, ["111", '222', '333'])
        session.flush()
        create_post(session, "post_caption", "test_post", 1,  ["111", "222"])
        session.commit()


  

if __name__ == "__main__":
    main()