from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func

from db import Base


class DateMixins(object):
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('CURRENT_TIMESTAMP'),
                        onupdate=func.now())


class User(Base, DateMixins):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
