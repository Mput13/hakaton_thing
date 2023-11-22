import datetime
from typing import Any

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from bot.models.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                                    index=True, unique=True)
    surname = sqlalchemy.Column(sqlalchemy.String,
                                    index=True, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                                    index=True, unique=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.String,
                                    index=True, unique=True)
    chat_id = sqlalchemy.Column(sqlalchemy.BigInteger,
                                    index=True, unique=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
