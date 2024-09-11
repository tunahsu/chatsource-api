import uuid
from typing import List

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship('OAuthAccount',
                                                              lazy='joined')
    # Establishing the one-to-many relationship
    chatbots = relationship('Chatbot',
                            back_populates='owner',
                            cascade='all, delete-orphan')


class Chatbot(Base):
    __tablename__ = 'chatbot'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    llm = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    instruction = Column(Text, nullable=False, default='')
    user_id = Column(UUID, ForeignKey('user.id'), nullable=False)

    # Establishing the many-to-one relationship
    owner = relationship('User', back_populates='chatbots')
