import uuid
import enum
from typing import List

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseOAuthAccountTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Column, String, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class UserRole(enum.Enum):
    owner = 'owner'
    member = 'member'


class UserChatbot(Base):
    __tablename__ = 'user_chatbot'

    user_id = mapped_column(GUID, ForeignKey('user.id'), primary_key=True)
    chatbot_id = Column(UUID, ForeignKey('chatbot.id'), primary_key=True)
    role = Column(Enum(UserRole), nullable=False)

    user = relationship('User', back_populates='chatbots')
    chatbot = relationship('Chatbot', back_populates='users')


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship('OAuthAccount',
                                                              lazy='joined')

    chatbots = relationship('UserChatbot',
                            back_populates='user',
                            cascade='all, delete-orphan')


class Chatbot(Base):
    __tablename__ = 'chatbot'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    llm = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    instruction = Column(Text, nullable=False, default='')

    users = relationship('UserChatbot',
                         back_populates='chatbot',
                         cascade='all, delete-orphan')
    documents = relationship('Document',
                             back_populates='chatbot',
                             cascade='all, delete-orphan')


class Document(Base):
    __tablename__ = 'document'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    chatbot_id = Column(UUID, ForeignKey('chatbot.id'))
    chatbot = relationship('Chatbot', back_populates='documents')
