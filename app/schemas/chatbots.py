import uuid
from pydantic import BaseModel


class BaseRequestDBModel(BaseModel):

    class Config:
        from_attributes = True


class BaseResponseModel(BaseModel):
    id: uuid.UUID

    class Config:
        from_attributes = True
        from_orm = True


class ChatbotCreateRequest(BaseRequestDBModel):
    name: str
    llm: str
    temperature: float
    instruction: str


class ChatbotCreateResponse(BaseResponseModel):
    name: str
    llm: str
    temperature: float
    instruction: str
    # members: list


class ChatbotQueryRequest(BaseRequestDBModel):
    id: uuid.UUID
    content: str


class ChatbotTrainRequest(BaseRequestDBModel):
    title: str
    content: str
    chatbot_id: uuid.UUID


class ChatbotTrainReponse(BaseResponseModel):
    title: str
    content: str
