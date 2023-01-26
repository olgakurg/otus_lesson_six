""" Домашнее задание
Создание моделей данных для сайта "Мой блог" на выбранную тему

Цель:
В этой самостоятельной работе тренируем умения:

Создавать модели данных
Создавать связи между моделями
Работать с сессией
Делать простые запросы
Смысл:
Для того чтобы работать с SQLAlchemy в проектах с базой данных. Понимать как работать с orm
Создать модели Post, Tag для сайта "Мой блог" на тему (ваша тема). Для пользователя можно использовать стандартную модель User.
Установить связи между моделями.
Добавить некоторые данные.
Выбрать все посты конкретного пользователя с 2-мя любыми тегами

Описание/Пошаговая инструкция выполнения домашнего задания:
Создать новый проект "Мой блог", по нему будет 3 домашних задания. Рекомендуется создать для этого проекта отдельный репозиторий
Придумать тему блога. Она может быть любая какая вам более интересна (например экзотические птицы, занятия workout-ом, искусство, ...)
С помощью SQLAlchemy создать модели данных для блога, например (Post, User, ...) и все другие, которые вы считаете важными
Установить связи между моделями
В качестве примера ввести некоторые данные
Выбрать все посты конкретного пользователя, попробовать сделать другие запросы (Рекомендуется сделать это в виде тестов pytest, можно просто с помощью print)
Сдать дз в виде ссылки на репозиторий

Критерии оценки:
Задание считается выполненным, когда:
Создана модель данных, в ней есть хотя бы один класс. База заполняется данными через ORM
5 баллов
Дополнительно:
Есть пример запроса на выборку данных из базы (через ORM) (3 баллов)
Проверки реализованы в виде тестов на pytest (2 балла)
Итого 5 + 3 + 2 = максимально 10 баллов
"""

#Создать модели Post, Tag для сайта "Мой блог" на тему (ваша тема). 
#Для пользователя можно использовать стандартную модель User.
#Установить связи между моделями. - DONE

from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    false,
    func
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement = True)
    username = Column(String(32), nullable=False)
    archived = Column(Boolean, default=False, server_default=false())
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    _password = Column (String(32))
    posts = relationship("Post")
    

class Tag_Post(Base):
    __tablename__ = 'tags_posts'
    id = Column(Integer, primary_key=True, autoincrement = True)
    tag_id =  Column('tag_id', Integer, ForeignKey("tags.id"))
    post_id =  Column('post_id', Integer, ForeignKey("posts.id"))


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key = True, autoincrement = True)
    caption = Column(String(32), unique = True,  nullable=False)
    posts = relationship("Post", secondary = "tags_posts", back_populates= 'tags')
    


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement = True)
    title = Column(String(255), nullable=False)
    archived = Column(Boolean, default=False, server_default=false())
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    text = Column(Text, nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    tags = relationship('Tag', secondary = "tags_posts", back_populates="posts")

    def __str__(self):
        return f'id {self.id}, title = {self.title}, user_id = {self.user_id}, tags = {self.tags}'

    def __repr__(self):
        return self.__str__()