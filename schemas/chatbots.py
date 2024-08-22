from pydantic import BaseModel


class BaseDBModel(BaseModel):

    class Config:
        from_attributes = True


class BaseResponseModel(BaseModel):
    id: int

    class Config:
        from_attributes = True
        from_orm = True


class ChatbotCreate(BaseDBModel):
    chatbot_name: str
    llm_name: str
    llm_api_key: str
    temperature: float
    instructions: str


class ChatbotUpdate(BaseDBModel):
    chatbot_name: str
    llm_name: str
    llm_api_key: str
    temperature: float
    instructions: str


class ChatbotRequest(BaseDBModel):
    chatbot_name: str
    llm_name: str
    llm_api_key: str
    temperature: float
    instructions: str
    query: str


class ChatbotResponse(BaseResponseModel):
    chatbot_id: str
    chatbot_name: str
    llm_name: str
    llm_api_key: str
    temperature: float
    instructions: str
