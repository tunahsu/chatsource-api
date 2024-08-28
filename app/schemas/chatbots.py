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
    api_key: str
    temperature: float
    instruction: str


class ChatbotUpdate(BaseDBModel):
    name: str
    llm: str
    api_key: str
    temperature: float
    instruction: str


class ChatbotRequest(BaseDBModel):
    name: str
    llm: str
    api_key: str
    temperature: float
    instruction: str
    query: str


class ChatbotResponse(BaseResponseModel):
    name: str
    llm: str
    api_key: str
    temperature: float
    instruction: str
