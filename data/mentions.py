import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Mention(SqlAlchemyBase):
    __tablename__ = 'mentions'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime)
    startup_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("startups.id"))
