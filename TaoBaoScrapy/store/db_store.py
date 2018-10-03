# -*- coding: utf-8 -*-
# @Time    : 2018/10/2 下午10:34
# @Author  : JackColor
# @File    : db_store.py
# @Software: PyCharm
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(256))
    song_id = Column(Integer)
    song_name = Column(String(128))
    song_link = Column(String(512))
    author_name = Column(String(128))
    song_album_name = Column(String(256))


def init_db():
    engine = create_engine("mysql+pymysql://root:1234@47.96.110.95:3306/music?charset=utf8",
                           max_overflow=5,
                           pool_size=5,
                           )

    Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)


#

if __name__ == '__main__':
    init_db()
