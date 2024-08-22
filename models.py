import uuid
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
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

    # Establishing the one-to-many relationship
    chatbots = relationship('Chatbot',
                            back_populates='owner',
                            cascade='all, delete-orphan')


class Chatbot(Base, DateMixins):
    __tablename__ = 'chatbots'

    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(String, unique=True, index=True)
    chatbot_name = Column(String, nullable=False)
    llm_name = Column(String, nullable=False)
    llm_api_key = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    instructions = Column(Text, nullable=False, default='')
    is_active = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Establishing the many-to-one relationship
    owner = relationship('User', back_populates='chatbots')
