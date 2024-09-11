import uuid
from pydantic import BaseModel


class BaseDBModel(BaseModel):

    class Config:
        from_attributes = True


class BaseResponseModel(BaseModel):
    id: uuid.UUID

    class Config:
        from_attributes = True
        from_orm = True


class ChatbotCreate(BaseDBModel):
    name: str
    llm: str
    temperature: float
    instruction: str


class ChatbotUpdate(BaseDBModel):
    name: str
    llm: str
    temperature: float
    instruction: str


class ChatbotResponse(BaseResponseModel):
    name: str
    llm: str
    temperature: float
    instruction: str


class ChatbotQuery(BaseDBModel):
    id: uuid.UUID
    content: str
